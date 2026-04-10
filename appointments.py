import flet as ft
from db_connector import (
    get_all_appointments, 
    save_appointment, 
    delete_appointment, 
    update_appointment,
    get_patients_lookup,
    get_doctors_lookup
)

class AppointmentsUI:
    def __init__(self, page: ft.Page, name: str, role: str):
        self.page = page
        self.name = name
        self.role = role
        self.editing_id = None
        self.appt_list = ft.ListView(expand=True, spacing=10)

    def build(self):
        self.load_appointments()

        return ft.Container(
            expand=True,
            bgcolor="#F4F7F6",
            padding=30,
            border_radius=30,
            content=ft.Column([
                ft.Row([
                    ft.Column([
                        ft.Text("Daily Schedule", size=30, weight="bold", color="#2C3E50"),
                        ft.Text("Manage Patient Visits", color="black54"),
                    ]),
                    ft.Container(expand=True),
                    ft.ElevatedButton(
                        "Schedule New", 
                        icon=ft.Icons.ADD, 
                        bgcolor="#1b6a60", 
                        color="white",
                        on_click=lambda _: self.open_appt_form()
                    )
                ]),
                ft.Divider(height=20, color="transparent"),
                ft.Container(expand=True, content=self.appt_list)
            ])
        )

    def load_appointments(self):
        self.appt_list.controls.clear()
        records = get_all_appointments()
        for rec in records:
            # rec: (id, time, p_name, d_name, dept, status, p_id, d_id)
            if len(rec) == 8:
                self.appt_list.controls.append(self._appointment_node(*rec))
        self.page.update()

    def _appointment_node(self, appt_id, time, p_name, d_name, dept, status, p_id, d_id):
        # Determine color based on status
        status_colors = {
            "Confirmed": "#27ae60",
            "Pending": "#f39c12",
            "Cancelled": "#e74c3c"
        }
        dot_color = status_colors.get(status, "grey")

        return ft.Row([
            ft.Container(
                content=ft.Text(str(time), weight="bold", size=12, color="#2C3E50"), 
                width=100
            ),
            ft.Column([
                ft.Container(width=12, height=12, bgcolor=dot_color, border_radius=10),
                ft.Container(width=2, expand=True, bgcolor="#E0E0E0"),
            ], horizontal_alignment="center", spacing=0),
            ft.Container(
                expand=True, 
                padding=15, 
                bgcolor="white", 
                border_radius=15,
                border=ft.border.all(1, "#F0F0F0"),
                content=ft.Row([
                    ft.Column([
                        ft.Text(p_name, weight="bold", size=16, color="black"),
                        ft.Text(f"Dr. {d_name} ({dept})", size=13, color="black54"),
                    ], expand=True),
                    ft.Chip(
                        label=ft.Text(status, size=11, color="white"), 
                        bgcolor=dot_color
                    ),
                   
                    ft.PopupMenuButton(
                        icon_color="black",
                        items=[
                            ft.PopupMenuItem(
                                content="Edit Appointment", 
                                icon=ft.Icons.EDIT,
                                on_click=lambda _: self.open_appt_form(appt_id, p_id, d_id, dept, str(time), status)
                            ),
                            ft.PopupMenuItem(
                                content="Delete/Cancel", 
                                icon=ft.Icons.DELETE_OUTLINE,
                                on_click=lambda _: self.handle_delete(appt_id)
                            ),
                        ]
                    )
                ])
            )
        ], height=100)

    def open_appt_form(self, appt_id=None, p_id=None, d_id=None, dept="", time="", status="Confirmed"):
        self.editing_id = appt_id
        
        patients = get_patients_lookup()
        doctors = get_doctors_lookup()

        patient_dropdown = ft.Dropdown(
            label="Select Patient",
            value=str(p_id) if p_id else None,
            options=[ft.dropdown.Option(key=str(p[0]), text=p[1]) for p in patients]
        )
        doctor_dropdown = ft.Dropdown(
            label="Assign Doctor",
            value=str(d_id) if d_id else None,
            options=[ft.dropdown.Option(key=str(d[0]), text=d[1]) for d in doctors]
        )
        dept_field = ft.TextField(label="Department", value=dept)
        time_field = ft.TextField(label="Time (YYYY-MM-DD HH:MM:SS)", value=time)
        
        # Added this so you can change the status from "Pending"
        status_dropdown = ft.Dropdown(
            label="Status",
            value=status,
            options=[
                ft.dropdown.Option("Pending"),
                ft.dropdown.Option("Confirmed"),
                ft.dropdown.Option("Cancelled"),
            ]
        )

        def save_click(e):
            # Check if fields are filled
            if not patient_dropdown.value or not doctor_dropdown.value:
                return 

            if self.editing_id:
                success = update_appointment(
                    self.editing_id, 
                    patient_dropdown.value, 
                    doctor_dropdown.value, 
                    dept_field.value, 
                    time_field.value, 
                    status_dropdown.value
                )
            else:
                # For NEW appointments, i can now pass the selected status
                # (Note: might need to update save_appointment in db_connector to accept status incase i notice failiurs)
                success = save_appointment(
                    patient_dropdown.value, 
                    doctor_dropdown.value, 
                    dept_field.value, 
                    time_field.value
                )
            
            if success:
                dialog.open = False
                self.load_appointments()
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Edit Appointment" if appt_id else "New Appointment"),
            content=ft.Column([
                patient_dropdown, 
                doctor_dropdown, 
                dept_field, 
                time_field, 
                status_dropdown
            ], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: setattr(dialog, "open", False)),
                ft.ElevatedButton("Save", bgcolor="#1b6a60", color="white", on_click=save_click)
            ]
        )

        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def handle_delete(self, appt_id):
        if delete_appointment(appt_id):
            self.load_appointments()

def Appointments_UI(page, name, role):
    return AppointmentsUI(page, name, role).build()