import flet as ft
from patientspage import Patient_UI
from appointments import Appointments_UI
from paymentspage import Payments_UI
from employee import Employee_UI
from helppage import Help_UI
from settingspage import Settings_UI
from reportpage import BugReport_UI
from db_connector import get_dashboard_stats


class HomeUI:
    def __init__(self, page: ft.Page, name: str, role: str, logout_function):
        self.page = page
        self.name = name
        self.role = role
        self.logout_function = logout_function

        self.button_shape = ft.RoundedRectangleBorder(radius=30)

        result = get_dashboard_stats()
        self.patient_count = result["total_patients"]
        self.appointments_count = result["total_appointments"]
        self.doctors_count = result["total_doctors"]
        self.paid_count = result["paid_patients"]

        self._build_dashboard_cards()
        self._build_chat()

        self.main_container_holder = ft.Container(
            content=self._dashboard_view(),
            expand=True,
        )

        self._view = ft.Row(
            controls=[
                self._build_sidebar(),
                ft.Container(
                    content=self.main_container_holder,
                    expand=True,
                    padding=30,
                    bgcolor="#10302c",
                ),
            ],
            expand=True,
            spacing=0,
        )

    def build(self):
        """Return the root Flet control to be added to the page."""
        return self._view

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_dashboard_cards(self):
        self.total_patients_card = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.PERSON, color="white"),
                    ft.Text("Total Patients", color="white"),
                    ft.Text(f"{self.patient_count}", color="white", size=25),
                ],
                alignment="center",
                horizontal_alignment="center",
            ),
            bgcolor="#1b6a60",
            height=250,
            width=200,
            border_radius=15,
            expand=1,
            opacity=0.8,
        )

        self.appointments_card = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.EVENT_AVAILABLE, color="white"),
                    ft.Text("Appointments", color="white"),
                    ft.Text(f"{self.appointments_count}", color="white", size=25),
                ],
                alignment="center",
                horizontal_alignment="center",
            ),
            bgcolor="#f39c12",
            height=250,
            width=200,
            border_radius=15,
            expand=1,
            opacity=0.8,
        )

        self.doctors_card = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.MEDICATION, color="white"),
                    ft.Text("Doctors On-Duty", color="white"),
                    ft.Text(f"{self.doctors_count}", color="white", size=25),
                ],
                alignment="center",
                horizontal_alignment="center",
            ),
            bgcolor="#27ae60",
            height=250,
            width=200,
            border_radius=15,
            expand=1,
            opacity=0.8,
        )

        self.payments_card = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.PAYMENTS, color="white"),
                    ft.Text("Paid Patients", color="white"),
                    ft.Text(f"{self.paid_count}", color="white", size=25),
                ],
                alignment="center",
                horizontal_alignment="center",
            ),
            bgcolor="#e74c3c",
            height=250,
            width=200,
            border_radius=15,
            expand=1,
            opacity=0.8,
        )

    def _build_chat(self):
        self.chat_messages = ft.ListView(expand=True, spacing=10, auto_scroll=True)

        self.chat_input = ft.TextField(
            hint_text="Type a message to doctors...",
            expand=True,
            border_color="blue",
            border_radius=20,
            color="black",
        )

        self.chat_container = ft.Container(
            bgcolor="#585858",
            opacity=0.8,
            expand=2,
            border_radius=30,
            padding=20,
            content=ft.Column(
                [
                    ft.Text("Doctor Consultation", size=20, color="white"),
                    ft.Container(
                        bgcolor="#a5a5a5",
                        expand=True,
                        border_radius=15,
                        padding=15,
                        content=self.chat_messages,
                    ),
                    ft.Row(
                        [
                            self.chat_input,
                            ft.IconButton(
                                icon=ft.Icons.SEND,
                                icon_color="white",
                                on_click=self._send_message,
                            ),
                        ]
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    def _send_message(self, e):
        if self.chat_input.value != "":
            self.chat_messages.controls.append(
                ft.Text(
                    f"You: {self.chat_input.value}", color="#10302c", weight="bold"
                )
            )
            self.chat_input.value = ""
            self.page.update()

    def _dashboard_view(self):
        return ft.Column(
            [
                ft.Text("HMS Dashboard", size=24, color="#1b6a60"),
                ft.Row(
                    [
                        self.total_patients_card,
                        self.appointments_card,
                        self.doctors_card,
                        self.payments_card,
                    ],
                    spacing=20,
                ),
                ft.Divider(height=10, color="transparent"),
                ft.Row([self.chat_container], expand=True),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _change_view(self, e):
        clicked_title = e.control.title.value

        if clicked_title == "Dashboard":
            self.main_container_holder.content = self._dashboard_view()
            print("clicked")
        elif clicked_title == "Patients":
            self.main_container_holder.content = Patient_UI(
                self.page, self.name, self.role
            )
        elif clicked_title == "Appointments":
            self.main_container_holder.content = Appointments_UI(
                self.page, self.name, self.role
            )
        elif clicked_title == "Payments":
            self.main_container_holder.content = Payments_UI(
                self.page, self.name, self.role
            )
        elif clicked_title == "Employee":
            self.main_container_holder.content = Employee_UI(
                self.page, self.name, self.role
            )
        elif clicked_title == "Help & Center":
            self.main_container_holder.content = Help_UI(
                self.page, self.name, self.role
            )
        elif clicked_title == "Settings":
            self.main_container_holder.content = Settings_UI(
                self.page, self.name, self.role
            )
        elif clicked_title == "Report":
            self.main_container_holder.content = BugReport_UI(
                self.page, self.name, self.role
            )
        self.page.update()

    def _build_sidebar(self):
        btn = self.button_shape

        sidebar_column = ft.Column(
            controls=[
                ft.Text(" menu", size=15, color="white", margin=5),
                ft.Divider(thickness=1, color="white24"),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.DASHBOARD, color="white"),
                    title=ft.Text("Dashboard", color="white"),
                    shape=btn,
                    hover_color="white25",
                    on_click=self._change_view,
                ),
                ft.Divider(thickness=1, color="#0a341f"),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PERSON_PIN, color="white"),
                    title=ft.Text("Patients", color="white"),
                    shape=btn,
                    hover_color="white25",
                    on_click=self._change_view,
                ),
                ft.Divider(thickness=1, color="white10"),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.SCHEDULE_SEND_OUTLINED, color="white"),
                    title=ft.Text("Appointments", color="white"),
                    shape=btn,
                    hover_color="white25",
                    on_click=self._change_view,
                ),
                ft.Divider(thickness=1, color="white10"),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PAYMENT, color="white"),
                    title=ft.Text("Payments", color="white"),
                    shape=btn,
                    hover_color="white25",
                    on_click=self._change_view,
                ),
                ft.Divider(thickness=1, color="white10"),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.PEOPLE_ALT_SHARP, color="white"),
                    title=ft.Text("Employee", color="white"),
                    shape=btn,
                    hover_color="white25",
                    on_click=self._change_view,
                ),
                ft.Divider(thickness=1, color="white10"),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.HELP, color="white"),
                    title=ft.Text("Help & Center", color="white"),
                    shape=btn,
                    hover_color="white25",
                    on_click=self._change_view,
                ),
                ft.Divider(thickness=1, color="white10"),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.SETTINGS_OUTLINED, color="white"),
                    title=ft.Text("Settings", color="white"),
                    shape=btn,
                    hover_color="white25",
                    on_click=self._change_view,
                ),
                ft.Divider(thickness=1, color="white10"),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BUG_REPORT, color="white"),
                    title=ft.Text("Report", color="white"),
                    shape=btn,
                    hover_color="white45",
                    on_click=self._change_view,
                ),
                ft.Container(expand=True),
                ft.Divider(thickness=1, color="white24"),
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.LOGOUT, color="white"),
                    title=ft.Text("Logout", color="white"),
                    shape=btn,
                    hover_color="white10",
                    on_click=lambda _: self.logout_function(),
                ),
            ],
            spacing=0,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

        return ft.Container(
            content=sidebar_column,
            width=250,
            bgcolor="#0d221f",
            padding=0,
            opacity=0.8,
        )


# ---------------------------------------------------------------------------
# Backwards-compatibility shim — keeps any code that still calls Home_UI(...)
# working without changes.
# ---------------------------------------------------------------------------
def Home_UI(page, name, role, logout_function):
    return HomeUI(page, name, role, logout_function).build()