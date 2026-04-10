import flet as ft


class HelpUI:
    def __init__(self, page: ft.Page, name: str, role: str):
        self.page = page
        self.name = name
        self.role = role

    def build(self):
        help_content = ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("How can we help you?", size=28, weight="bold", color="white"),
                    ft.TextField(
                        hint_text="Search for guides, troubleshooting, etc...",
                        prefix_icon=ft.Icons.SEARCH,
                        bgcolor="white",
                        border_radius=10,
                        width=500,
                    )
                ], horizontal_alignment="center"),
                bgcolor="#1b6a60",
                padding=40,
                border_radius=20,
                alignment=ft.Alignment.CENTER,
            ),
            ft.Divider(height=30, color="transparent"),
            ft.Text("Popular Topics", size=20, weight="bold", color="#2C3E50"),
            ft.Row([
                self._help_card("Getting Started", "Learn the basics of the HMS.", ft.Icons.ROCKET_LAUNCH, "blue"),
                self._help_card("Patient Records", "How to add and edit patients.", ft.Icons.PERSON_ADD, "green"),
                self._help_card("Billing & Payments", "Managing invoices and revenue.", ft.Icons.PAYMENTS, "orange"),
            ], spacing=20),
            ft.Row([
                self._help_card("Scheduling", "Managing doctor appointments.", ft.Icons.CALENDAR_MONTH, "purple"),
                self._help_card("Staff Management", "How to manage employee roles.", ft.Icons.BADGE, "red"),
                self._help_card("Security", "Password and data protection.", ft.Icons.LOCK, "grey"),
            ], spacing=20),
            ft.Divider(height=30, color="transparent"),
            ft.Container(
                padding=20,
                bgcolor="white",
                border_radius=15,
                border=ft.border.all(1, "#1b6a60"),
                content=ft.Row([
                    ft.Icon(ft.Icons.SUPPORT_AGENT, size=40, color="#1b6a60"),
                    ft.Column([
                        ft.Text("Still need help?", weight="bold", size=18),
                        ft.Text("Our technical support team is available 24/7 for hospital staff.", size=14),
                    ], expand=True),
                    ft.ElevatedButton("Contact Support", bgcolor="#1b6a60", color="white")
                ])
            )
        ], spacing=10)

        return ft.Container(
            expand=True,
            bgcolor="#F4F7F6",
            padding=30,
            border_radius=30,
            content=ft.ListView(
                [help_content],
                expand=True,
                spacing=10,
            ),
        )

    def _help_card(self, title, description, icon, color):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon, size=30, color=color),
                ft.Text(title, weight="bold", size=16, color="black"),
                ft.Text(description, size=12, color="black54", text_align="center"),
            ], alignment="center", horizontal_alignment="center"),
            bgcolor="white",
            padding=20,
            border_radius=15,
            border=ft.border.all(1, "#eeeeee"),
            expand=1,
            on_hover=lambda e: setattr(e.control, "elevation", 5 if e.data == "true" else 0),
        )


def Help_UI(page, name, role):
    return HelpUI(page, name, role).build()
