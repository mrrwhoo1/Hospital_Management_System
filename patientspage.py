import flet as ft
from db_connector import get_all_patients, delete_patient, save_patient, search_patients, update_patient


class PatientUI:
    def __init__(self, page: ft.Page, name: str, role: str):
        self.page = page
        self.name = name
        self.role = role
        self.editing_id = None  # Tracks if we are editing an existing patient

        self.patient_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
            auto_scroll=False,
        )

        self._build_form_fields()
        self._build_dialog()

    def build(self):
        self._load_patient_data()

        search_input = ft.TextField(
            hint_text="Search by name...",
            border_radius=30,
            expand=True,
            on_submit=lambda e: self._handle_search(search_input),
        )
        search_button = ft.IconButton(
            icon=ft.Icons.SEND,
            icon_color="white",
            on_click=lambda e: self._handle_search(search_input),
        )

        self._search_input = search_input

        return ft.Container(
            expand=True,
            border_radius=30,
            content=ft.Stack([
                ft.Column([
                    ft.Row([search_input, search_button]),
                    ft.Text("Patient Registry", size=20, weight="bold"),
                    ft.Divider(),
                    self.patient_list,
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.FloatingActionButton(
                    icon=ft.Icons.ADD,
                    bgcolor="#1b6a60",
                    tooltip="Add New Patient",
                    on_click=self._open_add_modal,
                    bottom=30,
                    right=30,
                ),
            ]),
        )

    def _build_form_fields(self):
        self.new_name = ft.TextField(label="Full Name", prefix_icon=ft.Icons.PERSON)
        self.new_age = ft.TextField(label="Age", width=140)
        self.new_billing = ft.Dropdown(
            label="Billing Type",
            expand=True,
            options=[ft.dropdown.Option("Paid"), ft.dropdown.Option("Free")],
        )
        self.new_contact = ft.TextField(label="Contact Number", prefix_icon=ft.Icons.PHONE)
        self.new_email = ft.TextField(label="Email", prefix_icon=ft.Icons.EMAIL)
        self.new_address = ft.TextField(label="Home Address", multiline=True, min_lines=2)
        self.new_symptoms = ft.TextField(label="Symptoms", multiline=True, min_lines=2)

    def _build_dialog(self):
        self.add_dialog = ft.AlertDialog(
            title=ft.Text("Patient Details"),
            content=ft.Container(
                width=600,
                content=ft.Column([
                    self.new_name,
                    ft.Row([self.new_age, self.new_billing], spacing=10),
                    ft.Row([self.new_contact, self.new_email], spacing=10),
                    self.new_address,
                    self.new_symptoms,
                ], tight=True, spacing=10),
            ),
            actions=[
                ft.TextButton(
                    "Cancel",
                    on_click=lambda _: self._close_dialog(),
                ),
                ft.ElevatedButton(
                    "Save Record",
                    bgcolor="#1b6a60",
                    color="white",
                    on_click=self._handle_save_process,
                ),
            ],
        )

    def _load_patient_data(self, search_query=None):
        self.patient_list.controls.clear()
        real_patients = (
            search_patients(search_query) if search_query else get_all_patients()
        )
        if real_patients:
            for p in real_patients:
                # Assuming get_all_patients returns (id, name, age, contact, billing)
                self.patient_list.controls.append(
                    self._create_patient_card(p[0], p[1], p[2], p[3], p[4])
                )
        self.page.update()

    def _create_patient_card(self, db_id, n, a, c, b):
        return ft.Container(
            content=ft.ListTile(
                leading=ft.Icon(ft.Icons.PERSON_OUTLINE, color="#1b6a60"),
                title=ft.Text(n, weight="bold", color="black"),
                subtitle=ft.Text(f"ID: {db_id} | Age: {a} | Contact: {c} | {b}", color="black"),
                trailing=ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(
                            content="Edit",
                            icon=ft.Icons.EDIT,
                            on_click=lambda _: self._open_edit_modal(db_id, n, a, c, b),
                        ),
                        ft.PopupMenuItem(
                            content="Delete",
                            icon=ft.Icons.DELETE,
                            on_click=lambda _, did=db_id: self._handle_delete(did),
                        ),
                    ]
                ),
            ),
            bgcolor="#D5D9D8",
            border_radius=10,
            border=ft.border.all(1, "#117053"),
        )

    def _handle_save_process(self, e):
        # Determine if we are updating or inserting
        if self.editing_id:
            res = update_patient(
                self.editing_id,
                self.new_name.value,
                self.new_age.value,
                self.new_contact.value,
                self.new_email.value,
                self.new_address.value,
                self.new_symptoms.value,
                self.new_billing.value,
            )
            msg = "Record Updated!"
        else:
            res = save_patient(
                self.new_name.value,
                self.new_age.value,
                self.new_contact.value,
                self.new_email.value,
                self.new_address.value,
                self.new_symptoms.value,
                self.new_billing.value,
            )
            msg = f"Patient {self.new_name.value} Registered!"

        if res:
            self._close_dialog()
            self.page.snack_bar = ft.SnackBar(ft.Text(msg), bgcolor="green")
            self.page.snack_bar.open = True
            self._load_patient_data()
        self.page.update()

    def _open_add_modal(self, e):
        self.editing_id = None  # Reset editing ID
        self.add_dialog.title.value = "Register New Patient"
        self._clear_form()
        self._show_dialog()

    def _open_edit_modal(self, db_id, n, a, c, b):
        self.editing_id = db_id
        self.add_dialog.title.value = f"Edit Patient: {n}"
        
        # Fill form with existing data
        self.new_name.value = n
        self.new_age.value = a
        self.new_contact.value = c
        self.new_billing.value = b
        # (Note: address, email, symptoms aren't in the card, 
        # so they stay blank unless you fetch them by ID first)
        
        self._show_dialog()

    def _show_dialog(self):
        if self.add_dialog not in self.page.overlay:
            self.page.overlay.append(self.add_dialog)
        self.add_dialog.open = True
        self.page.update()

    def _close_dialog(self):
        self.add_dialog.open = False
        self._clear_form()
        self.page.update()

    def _clear_form(self):
        for field in [
            self.new_name, self.new_age, self.new_contact,
            self.new_email, self.new_address, self.new_symptoms,
        ]:
            field.value = ""
        self.new_billing.value = None

    def _handle_search(self, search_input):
        self._load_patient_data(search_input.value)

    def _handle_delete(self, db_id):
        if delete_patient(db_id):
            self._load_patient_data()


def Patient_UI(page, name, role):
    return PatientUI(page, name, role).build()