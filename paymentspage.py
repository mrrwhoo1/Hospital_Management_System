import flet as ft
from db_connector import (
    get_all_payments, 
    save_payment, 
    get_payment_summary, 
    get_all_patients_simple,
    delete_payment,
    search_payments
)

class PaymentsUI:
    def __init__(self, page: ft.Page, name: str, role: str):
        self.page = page
        self.name = name
        self.role = role
        self.transaction_list = ft.ListView(expand=True, spacing=0)

    def build(self):
        # Fetch actual stats from DB
        stats = get_payment_summary()
        
        payment_stats = ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text("Total Revenue", color="white70"),
                    ft.Text(f"K {stats['total_revenue']:,}", size=20, weight="bold", color="white"),
                ]),
                bgcolor="#1b6a60", padding=15, border_radius=12, expand=1,
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Pending Invoices", color="#7f8c8d"),
                    ft.Text(str(stats['pending_count']), size=20, weight="bold", color="#e74c3c"),
                ]),
                bgcolor="white", border=ft.border.all(1, "#E0E0E0"),
                padding=15, border_radius=12, expand=1,
            ),
        ])

        self.load_payments()

        return ft.Container(
            expand=True,
            border_radius=30,
            bgcolor="#F4F7F6",
            padding=30,
            content=ft.Column([
                ft.Row([
                    ft.Text("Financial Management", size=28, weight="bold", color="#2C3E50"),
                    ft.Container(expand=True),
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD, 
                        bgcolor="#1b6a60",
                        content="New Payment",
                        on_click=lambda _: self.open_payment_modal()
                    )
                ]),
                payment_stats,
                ft.Divider(height=20, color="transparent"),
                ft.Row([
                    ft.Text("Recent Transactions", size=18, weight="bold", color="#2C3E50"),
                    ft.Container(expand=True),
                    ft.TextField(
                        hint_text="Search patient...", 
                        width=200, 
                        height=40, 
                        text_size=12,
                        on_change=lambda e: self.load_payments(e.control.value)
                    ),
                ]),
                ft.Container(
                    expand=True,
                    bgcolor="white",
                    border_radius=15,
                    border=ft.border.all(1, "#E0E0E0"),
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    content=self.transaction_list,
                ),
            ]),
        )

    def load_payments(self, search_query=None):
        self.transaction_list.controls.clear()
        # Fetch from db_connector
        data = search_payments(search_query) if search_query else get_all_payments()
        
        for row in data:
            # row format: (id, patient_name, amount, method, status, date)
            self.transaction_list.controls.append(
                self._transaction_row(row[0], row[1], row[3], row[2], row[4])
            )
        self.page.update()

    def _transaction_row(self, pay_id, name, method, amount, status):
        status_color = {
            "Paid": "green",
            "Pending": "#f39c12",
            "Overdue": "red"
        }.get(status, "grey")

        return ft.Container(
            padding=15,
            border=ft.border.only(bottom=ft.border.BorderSide(1, "#f0f0f0")),
            content=ft.Row([
                ft.Column([
                    ft.Text(f"PAY-{pay_id}", size=12, color="blue900", weight="bold"),
                    ft.Text(method, size=14, color="black54"),
                ], width=120),
                ft.Text(name, expand=True, size=14, color="black", weight="w500"),
                ft.Text(f"K {amount:,.2f}", width=120, weight="bold", text_align="right"),
                ft.Container(
                    content=ft.Text(status, size=10, color="white", weight="bold"),
                    bgcolor=status_color,
                    padding=ft.padding.symmetric(horizontal=10, vertical=4),
                    border_radius=5,
                    alignment=ft.Alignment.CENTER,
                    width=80,
                ),
                ft.PopupMenuButton(
                    icon_color="balck",
                    items=[
                        ft.PopupMenuItem(
                            content="Delete", 
                            icon=ft.Icons.DELETE_OUTLINE,
                            on_click=lambda _: self.handle_delete(pay_id)
                        ),
                    ]
                )
            ]),
        )

    def open_payment_modal(self):
        # Fetch patients for the dropdown
        patients = get_all_patients_simple()
        
        patient_dropdown = ft.Dropdown(
            label="Select Patient",
            options=[ft.dropdown.Option(key=str(p[0]), text=p[1]) for p in patients]
        )
        amount_field = ft.TextField(
    label="Amount (K)", 
    prefix=ft.Text("K "),
    keyboard_type=ft.KeyboardType.NUMBER )
        method_dropdown = ft.Dropdown(
            label="Payment Method",
            options=[
                ft.dropdown.Option("Cash"),
                ft.dropdown.Option("Card"),
                ft.dropdown.Option("Mobile Money"),
                ft.dropdown.Option("Insurance"),
            ]
        )
        status_dropdown = ft.Dropdown(
            label="Status",
            value="Paid",
            options=[
                ft.dropdown.Option("Paid"),
                ft.dropdown.Option("Pending"),
            ]
        )
        notes_field = ft.TextField(label="Notes")

        def save_click(e):
            if not patient_dropdown.value or not amount_field.value:
                return
            
            success = save_payment(
                patient_dropdown.value,
                amount_field.value,
                method_dropdown.value,
                status_dropdown.value,
                notes_field.value
            )
            if success:
                dialog.open = False
                self.load_payments()
                self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Record New Payment"),
            content=ft.Column([
                patient_dropdown,
                amount_field,
                method_dropdown,
                status_dropdown,
                notes_field
            ], tight=True),
            actions=[
                ft.TextButton("Cancel", on_click=lambda _: setattr(dialog, "open", False)),
                ft.ElevatedButton("Save Payment", bgcolor="#1b6a60", color="white", on_click=save_click)
            ]
        )

        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()

    def handle_delete(self, pay_id):
        if delete_payment(pay_id):
            self.load_payments()

def Payments_UI(page, name, role):
    return PaymentsUI(page, name, role).build()