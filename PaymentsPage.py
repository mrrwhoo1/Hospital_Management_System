import threading
import customtkinter as ck
from db_connector import (
    get_all_payments, delete_payment, search_payments,
    get_payment_summary, get_all_patients_simple, save_payment
)

COL_WEIGHTS = [1, 3, 2, 2, 2, 2, 1]  # ID, Patient, Amount, Method, Status, Date, Actions
BATCH_SIZE  = 5

STATUS_COLORS = {
    "Paid":    "#2ecc71",
    "Pending": "#e67e22",
    "Overdue": "#e74c3c",
}


class PaymentsPage(ck.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self._row_pool:    list[dict] = []
        self._pending_data: list      = []
        self._batch_job               = None
        self._fetch_thread            = None

        # ── 1. Header ─────────────────────────────────────────────────
        header = ck.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 5))

        ck.CTkLabel(
            header, text="Payments",
            font=("Serifa BT", 28, "bold"), text_color="#1b6a60"
        ).pack(side="left")

        ck.CTkButton(
            header, text="+ Record Payment", width=150,
            fg_color="#1b6a60", hover_color="#35988b",
            font=("Serifa BT", 14), command=self.open_add_payment
        ).pack(side="right", padx=(10, 0))

        self.SearchEntry = ck.CTkEntry(
            header, placeholder_text="Search by patient name...", width=280
        )
        self.SearchEntry.pack(side="right", padx=10)
        self.SearchEntry.bind("<Return>", lambda e: self.refresh_list())

        ck.CTkButton(
            header, text="Search", width=80,
            fg_color="#1b6a60", command=self.refresh_list
        ).pack(side="right")

        # ── 2. Summary Cards ──────────────────────────────────────────
        self.SummaryFrame = ck.CTkFrame(self, fg_color="transparent")
        self.SummaryFrame.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))

        self._summary_labels = {}
        cards = [
            ("total_revenue", "Total Revenue",  "#1b6a60"),
            ("paid_count",    "Paid",            "#2ecc71"),
            ("pending_count", "Pending",         "#e67e22"),
            ("overdue_count", "Overdue",         "#e74c3c"),
        ]
        for key, title, color in cards:
            card = ck.CTkFrame(self.SummaryFrame, fg_color=color, corner_radius=12)
            card.pack(side="left", fill="both", expand=True, padx=5)
            ck.CTkLabel(card, text=title, font=("Segoe UI", 11),
                        text_color="white").pack(pady=(10, 0))
            val_lbl = ck.CTkLabel(card, text="—", font=("Serifa BT", 22, "bold"),
                                  text_color="white")
            val_lbl.pack(pady=(0, 10))
            self._summary_labels[key] = val_lbl

        # ── 3. Table Header ───────────────────────────────────────────
        self.TableHeader = ck.CTkFrame(self, fg_color="#1b6a60", height=40, corner_radius=0)
        self.TableHeader.grid(row=2, column=0, sticky="ew", padx=20)

        cols = ["ID", "Patient", "Amount (K)", "Method", "Status", "Date", "Actions"]
        for i, (name, w) in enumerate(zip(cols, COL_WEIGHTS)):
            self.TableHeader.grid_columnconfigure(i, weight=w)
            ck.CTkLabel(
                self.TableHeader, text=name,
                text_color="white", font=("Serifa BT", 13, "bold")
            ).grid(row=0, column=i, pady=5, sticky="ew")

        # ── 4. Loading label ──────────────────────────────────────────
        self.LoadingLabel = ck.CTkLabel(
            self, text="Loading payments...",
            font=("Segoe UI", 13), text_color="#888888"
        )
        self.LoadingLabel.grid(row=3, column=0, pady=40)

        # ── 5. Scrollable list ────────────────────────────────────────
        self.ListArea = ck.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        for i, w in enumerate(COL_WEIGHTS):
            self.ListArea.grid_columnconfigure(i, weight=w)

        self.after(50, self._load_all)

    # ── Load summary + list together ──────────────────────────────────

    def _load_all(self):
        self.refresh_summary()
        self.refresh_list()

    # ── Summary cards ─────────────────────────────────────────────────

    def refresh_summary(self):
        def _fetch():
            summary = get_payment_summary()
            self.after(0, lambda: self._apply_summary(summary))

        threading.Thread(target=_fetch, daemon=True).start()

    def _apply_summary(self, s: dict):
        self._summary_labels["total_revenue"].configure(
            text=f"K {s.get('total_revenue', 0):,.2f}"
        )
        self._summary_labels["paid_count"].configure(text=str(s.get("paid_count", 0)))
        self._summary_labels["pending_count"].configure(text=str(s.get("pending_count", 0)))
        self._summary_labels["overdue_count"].configure(text=str(s.get("overdue_count", 0)))

    # ── Row pool ──────────────────────────────────────────────────────

    def _get_row(self, index: int) -> dict:
        if index < len(self._row_pool):
            return self._row_pool[index]

        frame = ck.CTkFrame(self.ListArea, fg_color="#f9f9f9", height=35, corner_radius=4)
        for i, w in enumerate(COL_WEIGHTS):
            frame.grid_columnconfigure(i, weight=w)

        labels = []
        for col in range(6):  # ID, Patient, Amount, Method, Status, Date
            lbl = ck.CTkLabel(
                frame, text="", text_color="#1a1a1a",
                font=("Segoe UI", 12), anchor="center"
            )
            lbl.grid(row=0, column=col, sticky="ew", padx=4, pady=4)
            labels.append(lbl)

        btn = ck.CTkButton(
            frame, text="Del", width=50, height=24,
            fg_color="#952321", hover_color="#701a18",
            font=("Segoe UI", 11), command=lambda: None
        )
        btn.grid(row=0, column=6, padx=6, pady=4)

        entry = {"frame": frame, "labels": labels, "btn": btn}
        self._row_pool.append(entry)
        return entry

    # ── Refresh list ──────────────────────────────────────────────────

    def refresh_list(self):
        if self._batch_job is not None:
            self.after_cancel(self._batch_job)
            self._batch_job = None

        if self._fetch_thread and self._fetch_thread.is_alive():
            return

        self.ListArea.grid_remove()
        self.LoadingLabel.grid(row=3, column=0, pady=40)
        self.LoadingLabel.configure(text="Loading payments...")

        search_term = self.SearchEntry.get().strip()

        def _do_fetch():
            try:
                data = search_payments(search_term) if search_term else get_all_payments()
            except Exception as e:
                data = []
                print(f"Fetch error: {e}")
            self.after(0, lambda: self._on_fetch_complete(data))

        self._fetch_thread = threading.Thread(target=_do_fetch, daemon=True)
        self._fetch_thread.start()

    def _on_fetch_complete(self, data: list):
        if not data:
            self.LoadingLabel.configure(text="No payments found.")
            for row in self._row_pool:
                if row["frame"].winfo_ismapped():
                    row["frame"].grid_remove()
            return

        for i in range(len(data), len(self._row_pool)):
            row = self._row_pool[i]
            if row["frame"].winfo_ismapped():
                row["frame"].grid_remove()

        self._pending_data = list(enumerate(data))
        self._render_next_batch()

    def _render_next_batch(self):
        if not self._pending_data:
            self.LoadingLabel.grid_remove()
            self.ListArea.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))
            self._batch_job = None
            return

        batch, self._pending_data = (
            self._pending_data[:BATCH_SIZE],
            self._pending_data[BATCH_SIZE:]
        )

        for i, item in batch:
            # item: (payment_id, patient_name, amount, method, status, created_at)
            pay_id = item[0]
            status = item[4]
            row    = self._get_row(i)

            for col_idx, value in enumerate(item):
                text = str(value)
                if col_idx == 2:                        # amount
                    text = f"K {float(value):,.2f}"
                if col_idx == 5 and value:              # date — trim to date only
                    text = str(value)[:10]
                row["labels"][col_idx].configure(
                    text=text,
                    text_color=STATUS_COLORS.get(status, "#1a1a1a") if col_idx == 4 else "#1a1a1a"
                )

            row["btn"].configure(command=lambda pid=pay_id: self.remove_payment(pid))

            if not row["frame"].winfo_ismapped():
                row["frame"].grid(
                    row=i, column=0, columnspan=len(COL_WEIGHTS),
                    sticky="ew", padx=4, pady=1
                )

        self._batch_job = self.after(0, self._render_next_batch)

    # ── Delete ────────────────────────────────────────────────────────

    def remove_payment(self, pay_id):
        def _do_delete():
            if delete_payment(pay_id):
                self.after(0, self._load_all)

        threading.Thread(target=_do_delete, daemon=True).start()

    # ── Add Payment Dialog ────────────────────────────────────────────

    def open_add_payment(self):
        win = ck.CTkToplevel(self)
        win.geometry("480x520")
        win.minsize(480, 520)
        win.title("Record Payment")
        win.attributes("-topmost", True)

        scroll = ck.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        form = ck.CTkFrame(scroll, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=20, pady=10)

        ck.CTkLabel(form, text="Record Payment",
                    font=("Serifa BT", 20, "bold"), text_color="#1b6a60").pack(anchor="w", pady=(0, 15))

        # Patient dropdown — pulled live from DB
        ck.CTkLabel(form, text="Patient", font=("Serifa BT", 14)).pack(anchor="w")
        patients = get_all_patients_simple()   # [(patient_id, full_name), ...]
        patient_names = [p[1] for p in patients]
        patient_map   = {p[1]: p[0] for p in patients}

        patient_var = ck.StringVar(value=patient_names[0] if patient_names else "No patients found")
        patient_menu = ck.CTkOptionMenu(form, variable=patient_var, values=patient_names, width=400)
        patient_menu.pack(pady=(0, 10))

        # Amount
        ck.CTkLabel(form, text="Amount (K)", font=("Serifa BT", 14)).pack(anchor="w")
        amount_entry = ck.CTkEntry(form, placeholder_text="e.g. 350.00", width=400)
        amount_entry.pack(pady=(0, 10))

        # Method
        ck.CTkLabel(form, text="Payment Method", font=("Serifa BT", 14)).pack(anchor="w")
        method_var = ck.StringVar(value="Cash")
        ck.CTkOptionMenu(form, variable=method_var,
                         values=["Cash", "Card", "Insurance", "Mobile Money"],
                         width=400).pack(pady=(0, 10))

        # Status
        ck.CTkLabel(form, text="Status", font=("Serifa BT", 14)).pack(anchor="w")
        status_var = ck.StringVar(value="Paid")
        status_row = ck.CTkFrame(form, fg_color="transparent")
        status_row.pack(fill="x", pady=(0, 10))
        for s, color in STATUS_COLORS.items():
            ck.CTkRadioButton(
                status_row, text=s, variable=status_var, value=s, fg_color=color
            ).pack(side="left", padx=(0, 15))

        # Notes
        ck.CTkLabel(form, text="Notes (optional)", font=("Serifa BT", 14)).pack(anchor="w")
        notes_box = ck.CTkTextbox(form, height=70, width=400, border_width=2)
        notes_box.pack(pady=(0, 15))

        # Error label
        err_lbl = ck.CTkLabel(form, text="", text_color="#e74c3c", font=("Segoe UI", 11))
        err_lbl.pack(anchor="w")

        def submit():
            patient_name = patient_var.get()
            amount_raw   = amount_entry.get().strip()
            method       = method_var.get()
            status       = status_var.get()
            notes        = notes_box.get("1.0", "end-1c").strip()

            if not patient_name or patient_name == "No patients found":
                err_lbl.configure(text="Please select a patient.")
                return
            try:
                amount = float(amount_raw)
                if amount <= 0:
                    raise ValueError
            except ValueError:
                err_lbl.configure(text="Enter a valid amount greater than 0.")
                return

            patient_id = patient_map.get(patient_name)

            def _do_save():
                ok = save_payment(patient_id, amount, method, status, notes)
                if ok:
                    self.after(0, lambda: [win.destroy(), self._load_all()])
                else:
                    self.after(0, lambda: err_lbl.configure(text="Database error. Try again."))

            threading.Thread(target=_do_save, daemon=True).start()

        # Buttons
        btn_row = ck.CTkFrame(form, fg_color="transparent")
        btn_row.pack(fill="x", pady=10)

        ck.CTkButton(btn_row, text="Cancel", fg_color="gray",
                     hover_color="#555", command=win.destroy
                     ).pack(side="left", expand=True, padx=5)

        ck.CTkButton(btn_row, text="Save Payment", fg_color="#1b6a60",
                     hover_color="#35988b", command=submit
                     ).pack(side="left", expand=True, padx=5)
