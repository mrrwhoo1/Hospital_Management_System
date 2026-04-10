import flet as ft


class SettingsUI:
    def __init__(self, page: ft.Page, name: str, role: str):
        self.page = page
        self.name = name
        self.role = role

    def build(self):
        settings_content = ft.Column([
            ft.Text("Settings", size=30, weight="bold", color="#2C3E50"),
            ft.Text("Manage your account preferences and system configuration", color="black54"),
            ft.Divider(height=20, color="transparent"),

            self._group_title("Account Security"),
            ft.Card(
                content=ft.Column([
                    self._setting_item("Profile Information", "Update your name and contact details", ft.Icons.PERSON, ft.IconButton(ft.Icons.ARROW_FORWARD_IOS, icon_size=15)),
                    ft.Divider(height=1, color="#F0F0F0"),
                    self._setting_item("Change Password", "Last changed 3 months ago", ft.Icons.LOCK_RESET, ft.ElevatedButton("Update")),
                    ft.Divider(height=1, color="#F0F0F0"),
                    self._setting_item("Two-Factor Authentication", "Secure your HMS account", ft.Icons.SHIELD_OUTLINED, ft.Switch(value=True, active_color="#1b6a60")),
                ], spacing=0),
            ),

            self._group_title("System Preferences"),
            ft.Card(
                content=ft.Column([
                    self._setting_item("Dark Mode", "Adjust the theme of the interface", ft.Icons.DARK_MODE, ft.Switch(value=False)),
                    ft.Divider(height=1, color="#F0F0F0"),
                    self._setting_item("Language", "Set your preferred language", ft.Icons.LANGUAGE, ft.Text("English (UK)", weight="bold")),
                    ft.Divider(height=1, color="#F0F0F0"),
                    self._setting_item("Auto-save Changes", "Automatically save form data", ft.Icons.SAVE, ft.Switch(value=True, active_color="#1b6a60")),
                ], spacing=0),
            ),

            self._group_title("Notifications"),
            ft.Card(
                content=ft.Column([
                    self._setting_item("Email Alerts", "Receive appointment reminders", ft.Icons.EMAIL_OUTLINED, ft.Switch(value=True)),
                    ft.Divider(height=1, color="#F0F0F0"),
                    self._setting_item("Desktop Notifications", "Show alerts on this computer", ft.Icons.DESKTOP_WINDOWS, ft.Switch(value=True)),
                ], spacing=0),
            ),

            ft.Divider(height=40, color="transparent"),
            ft.ElevatedButton(
                "Logout of all devices",
                icon=ft.Icons.LOGOUT,
                color="red",
                style=ft.ButtonStyle(overlay_color="red10"),
            ),
        ], spacing=10)

        return ft.Container(
            expand=True,
            border_radius=30,
            bgcolor="#F4F7F6",
            padding=30,
            content=ft.ListView([settings_content], expand=True, spacing=10),
        )

    def _group_title(self, text):
        return ft.Container(
            content=ft.Text(text, size=18, weight="bold", color="#1b6a60"),
            margin=ft.margin.only(top=20, bottom=10),
        )

    def _setting_item(self, title, subtitle, icon, control):
        return ft.ListTile(
            leading=ft.Icon(icon, color="#2C3E50"),
            title=ft.Text(title, weight="bold"),
            subtitle=ft.Text(subtitle, size=12),
            trailing=control,
        )


def Settings_UI(page, name, role):
    return SettingsUI(page, name, role).build()
