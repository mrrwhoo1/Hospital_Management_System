import os
import subprocess
import sys
import flet as ft
from db_connector import (
    get_all_payments,
    save_payment,
    get_payment_summary,
    get_all_patients_simple,
    delete_payment,
    search_payments,
    get_payment_full_details,      # ← new function added to db_connector
)
from receipt_generator import generate_receipt


class PaymentsUI:
    def __init__(self, page: ft.Page, name: str, role: str):
        self.page = page
        self.name = name
        self.role = role
        self.transaction_list = ft.ListView(expand=True, spacing=0)

    def build(self):
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

    # ── Load / display ────────────────────────────────────────────────────
    def load_payments(self, search_query=None):
        self.transaction_list.controls.clear()
        data = search_payments(search_query) if search_query else get_all_payments()

        for row in data:
            # row: (id, patient_name, amount, method, status, date)
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
                    icon_color="black",
                    items=[
                        ft.PopupMenuItem(
                            content="Print Receipt",
                            icon=ft.Icons.RECEIPT_LONG,
                            on_click=lambda _, pid=pay_id: self.print_receipt(pid)
                        ),
                        ft.PopupMenuItem(
                            content="Delete",
                            icon=ft.Icons.DELETE_OUTLINE,
                            on_click=lambda _, pid=pay_id: self.handle_delete(pid)
                        ),
                    ]
                )
            ]),
        )

    # ── Receipt generation ────────────────────────────────────────────────
    def print_receipt(self, pay_id: int):
        """Fetch full payment details, generate PDF, then open it."""
        details = get_payment_full_details(pay_id)

        if not details:
            self._show_snack("Could not find payment details.", "red")
            return

        # Build the data dict for the generator
        data = {
            "pay_id":        pay_id,
            "patient_name":  details.get("patient_name", "Unknown"),
            "patient_id":    details.get("patient_id", "—"),
            "age":           details.get("age", "—"),
            "contact":       details.get("contact", "—"),
            "email":         details.get("email", "—"),
            "address":       details.get("address", "—"),
            "symptoms":      details.get("symptoms", "—"),
            "amount":        details.get("amount", 0.0),
            "method":        details.get("method", "—"),
            "status":        details.get("status", "—"),
            "notes":         details.get("notes", ""),
            "date":          details.get("date"),
            "doctor_name":   details.get("doctor_name", "—"),
            "department":    details.get("department", "—"),
            "hospital_name": "SmartHealth Medical Centre",
        }

        # Save receipts inside a 'receipts' folder next to the app
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "receipts")
        try:
            pdf_path = generate_receipt(data, output_dir=output_dir)
            self._show_snack(f"Receipt saved: {os.path.basename(pdf_path)}", "#1b6a60")
            self._open_pdf(pdf_path)
        except Exception as ex:
            self._show_snack(f"Receipt error: {ex}", "red")

    def _open_pdf(self, path: str):
        """Open the PDF with the system default viewer (cross-platform)."""
        try:
            if sys.platform.startswith("win"):
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                # Linux — try xdg-open, evince, or okular
                for viewer in ["xdg-open", "evince", "okular", "mupdf"]:
                    if subprocess.run(["which", viewer], capture_output=True).returncode == 0:
                        subprocess.Popen([viewer, path])
                        break
        except Exception as ex:
            print(f"Could not auto-open PDF: {ex}")

    # ── Add payment modal ─────────────────────────────────────────────────
    def open_payment_modal(self):
        patients = get_all_patients_simple()

        patient_dropdown = ft.Dropdown(
            label="Select Patient",
            options=[ft.dropdown.Option(key=str(p[0]), text=p[1]) for p in patients]
        )
        amount_field = ft.TextField(
            label="Amount (K)",
            prefix=ft.Text("K "),
            keyboard_type=ft.KeyboardType.NUMBER
        )
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

    # ── Helpers ───────────────────────────────────────────────────────────
    def handle_delete(self, pay_id):
        if delete_payment(pay_id):
            self.load_payments()

    def _show_snack(self, message: str, color: str = "green"):
        self.page.snack_bar = ft.SnackBar(
            ft.Text(message, color="white"),
            bgcolor=color,
            duration=3000,
        )
        self.page.snack_bar.open = True
        self.page.update()


def Payments_UI(page, name, role):
    return PaymentsUI(page, name, role).build()