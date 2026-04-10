import flet as ft
from db_connector import db_connect_verifyer
from homepage import HomeUI


class SmartHealthApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self._setup_page()
        self._show_login()

    def _setup_page(self):
        self.page.title = "Smart Health"
        self.page.window_height = 1100
        self.page.window_width = 800
        self.page.padding = 0
        self.page.vertical_alignment = "center"
        self.page.horizontal_alignment = "center"

    # ------------------------------------------------------------------
    # Views
    # ------------------------------------------------------------------

    def _show_dashboard(self, name: str, role: str):
        self.page.clean()
        home = HomeUI(self.page, name, role, logout_function=self._show_login)
        self.page.add(home.build())
        self.page.update()

    def _show_login(self):
        self.page.controls.clear()

        username_field = ft.TextField(label="Username", border_radius=30)
        password_field = ft.TextField(
            label="Password",
            border_radius=30,
            password=True,
            can_reveal_password=True,
        )
        error_message = ft.Text(" ", color="red", size=12)

        def login(e):
            username = username_field.value
            password = password_field.value

            user_data = db_connect_verifyer(username, password)
            if user_data:
                role, name = user_data
                error_message.value = ""
                print(f"Success, name: {name} & user role: {role}")
                self._show_dashboard(name, role)
            else:
                error_message.value = "Invalid Username or Password. Please try again."
            self.page.update()

        background = ft.Container(
            expand=True,
            image=ft.DecorationImage(src="background.png", fit="cover"),
        )

        main_frame = ft.Container(
            width=500,
            height=400,
            bgcolor=ft.Colors.with_opacity(0.5, "#1b6eaa"),
            border_radius=30,
            padding=20,
            content=ft.Column(
                [
                    ft.Text("Smart Health", size=30, weight="bold", color="#1b6a60"),
                    ft.Text("Hospital Management System", size=20, color="#1b6a60"),
                    ft.Divider(height=20, color="transparent"),
                    username_field,
                    password_field,
                    error_message,
                    ft.Divider(height=1, color="transparent"),
                    ft.FilledButton(
                        "Login",
                        on_click=login,
                        height=40,
                        width=200,
                        style=ft.ButtonStyle(bgcolor="#1b6a60", color="white"),
                    ),
                ],
                horizontal_alignment="center",
                spacing=10,
            ),
        )

        login_ui = ft.Stack(
            expand=True,
            alignment=ft.Alignment(0, 0),
            controls=[background, main_frame],
        )

        self.page.add(login_ui)
        self.page.update()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def app(page: ft.Page):
    SmartHealthApp(page)


if __name__ == "__main__":
    ft.run(app, assets_dir="assets")