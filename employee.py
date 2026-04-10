import flet as ft
from db_connector import get_all_employees, search_employees, delete_employee, update_employee, add_user

class EmployeeUI:
    def __init__(self, page: ft.Page, name: str, role: str):
        self.page = page
        self.name = name
        self.role = role
        self.employee_list = ft.ListView(expand=True, spacing=10, padding=20)
        # Create the search field as a class variable to access its value later
        self.search_field = ft.TextField(
            hint_text="Search staff...", 
            width=250, 
            prefix_icon=ft.Icons.SEARCH,
            # Triggers search when 'Enter' is pressed
            on_submit=lambda e: self.load_employees(self.search_field.value) 
        )

    def build(self):
        self.load_employees()

        return ft.Container(
            expand=True,
            bgcolor="#F4F7F6",
            padding=30,
            border_radius=30,
            content=ft.Column([
                ft.Row([
                    ft.Text("Staff Directory", size=30, weight="bold", color="#2C3E50"),
                    ft.Container(expand=True),
                    # --- Search Group ---
                    ft.Row([
                        self.search_field,
                        ft.IconButton(
                            icon=ft.Icons.SEARCH,
                            bgcolor="#1b6a60",
                            icon_color="white",
                            tooltip="Search",
                            on_click=lambda _: self.load_employees(self.search_field.value)
                        ),
                        ft.IconButton(
                            icon=ft.Icons.REFRESH,
                            tooltip="Clear Search",
                            on_click=self.clear_search
                        ),
                    ], spacing=5),
                    # --- Add Button ---
                    ft.FloatingActionButton(
                        bgcolor="#1b6a60",
                        content=ft.Row([
                            ft.Icon(ft.Icons.ADD, color="white"),
                            ft.Text("Add Staff", color="white")
                        ], alignment="center", spacing=5),
                        width=130,
                        on_click=lambda _: self.open_employee_form()
                    )
                ]),
                ft.Divider(height=20),
                ft.Container(expand=True, content=self.employee_list)
            ])
        )

    def clear_search(self, e):
        """Clears the text field and reloads everyone."""
        self.search_field.value = ""
        self.load_employees()
        self.page.update()

    def load_employees(self, search_query=""):
        self.employee_list.controls.clear()
        
        # Use query if provided, otherwise fetch all
        if search_query and search_query.strip() != "":
            records = search_employees(search_query)
        else:
            records = get_all_employees()

        for rec in records:
            self.employee_list.controls.append(self._employee_card(*rec))
        
        self.page.update()

    # handle_search is no longer needed since we call load_employees directly from the button

    def _employee_card(self, user_id, full_name, username, role, email, phone, created_at):
        role_colors = {
            "Doctor": "#1b6a60", "Nurse": "#27ae60", "Admin": "#2980b9",
            "Pharmacist": "#8e44ad", "Receptionist": "#e67e22",
            "Janitor": "#7f8c8d", "Security": "#34495e"
        }
        dot_color = role_colors.get(role, "grey")

        return ft.Container(
            padding=10,
            bgcolor="white",
            border_radius=10,
            border=ft.border.all(1, "#eeeeee"),
            content=ft.ListTile(
                leading=ft.CircleAvatar(
                    content=ft.Text(full_name[0] if full_name else "?"),
                    bgcolor=dot_color,
                    color="white",
                ),
                title=ft.Text(full_name, weight="bold", color="black"),
                subtitle=ft.Text(f"{role} • {phone} • {email}", color="black54"),
                trailing=ft.Row([
                    ft.Container(
                        content=ft.Text("Active", size=10, color="white"),
                        bgcolor="green",
                        padding=ft.padding.symmetric(horizontal=8, vertical=2),
                        border_radius=5,
                    ),
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(
                                content="Edit Profile", 
                                icon=ft.Icons.EDIT,
                                on_click=lambda _: self.open_employee_form(user_id, full_name, username, role, email, phone)
                            ),
                            ft.PopupMenuItem(
                                content="Delete Staff", 
                                icon=ft.Icons.DELETE,
                                on_click=lambda _: self.delete_staff(user_id)
                            ),
                        ]
                    ),
                ], tight=True, spacing=5),
            ),
        )



    def delete_staff(self, user_id):
        # Call the DB function
        #print statements used for debugging
        if delete_employee(user_id):
            print(f"Deleted user {user_id}")
            self.load_employees() # Refresh UI
        else:
            print("Failed to delete user.")

    def open_employee_form(self, emp_id=None, full_name="", username="", role="Admin", email="", phone=""):
        print("clicked add staff")
        is_editing = emp_id is not None

        
        self.name_field = ft.TextField(label="Full Name", value=full_name, width=300)
        self.user_field = ft.TextField(label="Username", value=username, width=300)
        self.pass_field = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300, visible=not is_editing)
        self.role_field = ft.Dropdown(
            label="Role", 
            value=role, 
            width=300,
            options=[
                ft.dropdown.Option("Admin"), ft.dropdown.Option("Doctor"), 
                ft.dropdown.Option("Nurse"), ft.dropdown.Option("Pharmacist"),
                ft.dropdown.Option("Receptionist"), ft.dropdown.Option("Janitor"),
                ft.dropdown.Option("Security")
            ]
        )
        self.email_field = ft.TextField(label="Email", value=email, width=300)
        self.phone_field = ft.TextField(label="Phone", value=phone, width=300)

       
        def save_clicked(e):
            if is_editing:
                success = update_employee(emp_id, self.name_field.value, self.user_field.value, self.role_field.value, self.email_field.value, self.phone_field.value)
            else:
                success = add_user(self.user_field.value, self.pass_field.value, self.role_field.value, self.name_field.value, self.email_field.value, self.phone_field.value)
            
            if success:
                self.dialog.open = False
                self.load_employees() 
            else:
                print("Database operation failed.")
            self.page.update()

        
        self.dialog = ft.AlertDialog(
            title=ft.Text("Edit Staff" if is_editing else "Add New Staff"),
            content=ft.Container(
                width=400,
                content=ft.Column([
                    self.name_field, 
                    self.user_field, 
                    self.pass_field, 
                    self.role_field, 
                    self.email_field, 
                    self.phone_field
                ], tight=True, spacing=10),
            ),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: self.close_dialog()),
                ft.FilledButton("Save", on_click=save_clicked, bgcolor="#1b6a60", color="white"),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

       #use overlay to append to it
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()

    def close_dialog(self):
        self.dialog.open = False
        self.page.update()

def Employee_UI(page, name, role):
    return EmployeeUI(page, name, role).build()