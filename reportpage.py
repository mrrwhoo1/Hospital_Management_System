import flet as ft


class BugReportUI:
    def __init__(self, page: ft.Page, name: str, role: str):
        self.page = page
        self.name = name
        self.role = role

    def build(self):
        bug_form = ft.Container(
            padding=20,
            bgcolor="white",
            border_radius=15,
            border=ft.border.all(1, "#E0E0E0"),
            content=ft.Column([
                ft.Text("Submit New Ticket", size=18, weight="bold"),
                ft.TextField(label="Issue Title", hint_text="What's broken?", border_color="#1b6a60"),
                ft.TextField(label="Details", multiline=True, min_lines=2, max_lines=4),
                ft.ElevatedButton(
                    "Submit Report",
                    icon=ft.Icons.SEND,
                    bgcolor="#1b6a60",
                    color="white",
                    width=200,
                ),
            ], spacing=10),
        )

        ticket_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=ft.padding.only(top=10),
        )

        for i in range(1, 21):
            ticket_list.controls.append(
                ft.Container(
                    padding=10,
                    border=ft.border.all(1, "#eeeeee"),
                    border_radius=10,
                    bgcolor="white",
                    content=ft.ListTile(
                        leading=ft.Icon(ft.Icons.BUG_REPORT, color="red" if i % 2 == 0 else "orange"),
                        title=ft.Text(f"TKT-00{i}: Network error in Ward {i}"),
                        subtitle=ft.Text(f"Reported by: Staff_{i}"),
                        trailing=self._status_badge("Open" if i < 5 else "Resolved"),
                    ),
                )
            )

        return ft.Container(
            expand=True,
            bgcolor="#F4F7F6",
            padding=30,
            content=ft.Column([
                ft.Text("System Bug Tracker", size=28, weight="bold", color="#2C3E50"),
                bug_form,
                ft.Divider(height=30, color="transparent"),
                ft.Text("Ticket History", size=18, weight="bold"),
                ft.Container(expand=True, content=ticket_list),
            ]),
        )

    def _status_badge(self, status):
        colors = {"Open": "red", "In Progress": "orange", "Resolved": "green"}
        return ft.Container(
            content=ft.Text(status, size=10, color="white", weight="bold"),
            bgcolor=colors.get(status, "grey"),
            padding=ft.padding.symmetric(horizontal=10, vertical=4),
            border_radius=5,
        )


def BugReport_UI(page, name, role):
    return BugReportUI(page, name, role).build()
