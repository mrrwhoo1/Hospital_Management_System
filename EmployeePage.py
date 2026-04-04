import threading
import customtkinter as ck
from db_connector import get_all_employees, delete_employee,search_employees, update_employee, add_user, email_exists


COL_WEIGHTS = [1, 2, 2, 2, 2, 2, 1]  # ID, Full Name, Username, Role, Email, Phone, Actions
BATCH_SIZE  = 5

ROLES = ["Doctor", "Nurse", "Receptionist", "Admin", "Pharmacist", "Lab Technician"]
ROLE_COLORS = {
    "Doctor":          "#1b6a60",
    "Nurse":           "#2980b9",
    "Receptionist":    "#8e44ad",
    "Admin":           "#c0392b",
    "Pharmacist":      "#d35400",
    "Lab Technician":  "#27ae60",
}


class EmployeePage(ck.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._row_pool:     list[dict] = []
        self._pending_data: list       = []
        self._batch_job                = None
        self._fetch_thread             = None

        # ── 1. Header ─────────────────────────────────────────────────
        header = ck.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 5))

        ck.CTkLabel(
            header, text="Employees",
            font=("Serifa BT", 28, "bold"), text_color="#1b6a60"
        ).pack(side="left")

        ck.CTkButton(
            header, text="+ Add Employee", width=140,
            fg_color="#1b6a60", hover_color="#35988b",
            font=("Serifa BT", 14), command=self.open_add_employee
        ).pack(side="right", padx=(10, 0))

        self.SearchEntry = ck.CTkEntry(
            header, placeholder_text="Search by name...", width=280
        )
        self.SearchEntry.pack(side="right", padx=10)
        self.SearchEntry.bind("<Return>", lambda e: self.refresh_list())

        ck.CTkButton(
            header, text="Search", width=80,
            fg_color="#1b6a60", command=self.refresh_list
        ).pack(side="right")

        # ── 2. Table Header ───────────────────────────────────────────
        self.TableHeader = ck.CTkFrame(self, fg_color="#1b6a60", height=40, corner_radius=0)
        self.TableHeader.grid(row=1, column=0, sticky="ew", padx=20)

        cols = ["ID", "Full Name", "Username", "Role", "Email", "Phone", "Actions"]
        for i, (name, w) in enumerate(zip(cols, COL_WEIGHTS)):
            self.TableHeader.grid_columnconfigure(i, weight=w)
            ck.CTkLabel(
                self.TableHeader, text=name,
                text_color="white", font=("Serifa BT", 13, "bold")
            ).grid(row=0, column=i, pady=5, sticky="ew")

        # ── 3. Loading label ──────────────────────────────────────────
        self.LoadingLabel = ck.CTkLabel(
            self, text="Loading employees...",
            font=("Segoe UI", 13), text_color="#888888"
        )
        self.LoadingLabel.grid(row=2, column=0, pady=40)

        # ── 4. Scrollable list ────────────────────────────────────────
        self.ListArea = ck.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        for i, w in enumerate(COL_WEIGHTS):
            self.ListArea.grid_columnconfigure(i, weight=w)

        self.after(50, self.refresh_list)

    # ── Row pool ──────────────────────────────────────────────────────

    def _get_row(self, index: int) -> dict:
        if index < len(self._row_pool):
            return self._row_pool[index]

        frame = ck.CTkFrame(self.ListArea, fg_color="#f9f9f9", height=35, corner_radius=4)
        for i, w in enumerate(COL_WEIGHTS):
            frame.grid_columnconfigure(i, weight=w)

        labels = []
        for col in range(6):  # ID, Full Name, Username, Role, Email, Phone
            lbl = ck.CTkLabel(
                frame, text="", text_color="#1a1a1a",
                font=("Segoe UI", 12), anchor="center"
            )
            lbl.grid(row=0, column=col, sticky="ew", padx=4, pady=4)
            labels.append(lbl)

        # Edit + Delete buttons in last column
        action_frame = ck.CTkFrame(frame, fg_color="transparent")
        action_frame.grid(row=0, column=6, padx=6, pady=4)

        edit_btn = ck.CTkButton(
            action_frame, text="Edit", width=45, height=24,
            fg_color="#1b6a60", hover_color="#35988b",
            font=("Segoe UI", 11), command=lambda: None
        )
        edit_btn.pack(side="left", padx=(0, 3))

        del_btn = ck.CTkButton(
            action_frame, text="Del", width=45, height=24,
            fg_color="#952321", hover_color="#701a18",
            font=("Segoe UI", 11), command=lambda: None
        )
        del_btn.pack(side="left")

        entry = {"frame": frame, "labels": labels, "edit_btn": edit_btn, "del_btn": del_btn}
        self._row_pool.append(entry)
        return entry

    # ── Refresh ───────────────────────────────────────────────────────

    def refresh_list(self):
        if self._batch_job is not None:
            self.after_cancel(self._batch_job)
            self._batch_job = None

        if self._fetch_thread and self._fetch_thread.is_alive():
            return

        self.ListArea.grid_remove()
        self.LoadingLabel.grid(row=2, column=0, pady=40)
        self.LoadingLabel.configure(text="Loading employees...")

        search_term = self.SearchEntry.get().strip()

        def _do_fetch():
            try:
                data = search_employees(search_term) if search_term else get_all_employees()
            except Exception as e:
                data = []
                print(f"Fetch error: {e}")
            self.after(0, lambda: self._on_fetch_complete(data))

        self._fetch_thread = threading.Thread(target=_do_fetch, daemon=True)
        self._fetch_thread.start()

    def _on_fetch_complete(self, data: list):
        if not data:
            self.LoadingLabel.configure(text="No employees found.")
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
            self.ListArea.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
            self._batch_job = None
            return

        batch, self._pending_data = (
            self._pending_data[:BATCH_SIZE],
            self._pending_data[BATCH_SIZE:]
        )

        for i, item in batch:
            # item: (emp_id, full_name, username, role, email, phone, created_at)
            emp_id = item[0]
            role   = item[3]
            row    = self._get_row(i)

            for col_idx, value in enumerate(item[:6]):
                color = ROLE_COLORS.get(str(value), "#1a1a1a") if col_idx == 3 else "#1a1a1a"
                row["labels"][col_idx].configure(text=str(value), text_color=color)

            row["edit_btn"].configure(command=lambda eid=emp_id, d=item: self.open_edit_employee(eid, d))
            row["del_btn"].configure(command=lambda eid=emp_id: self.remove_employee(eid))

            if not row["frame"].winfo_ismapped():
                row["frame"].grid(
                    row=i, column=0, columnspan=len(COL_WEIGHTS),
                    sticky="ew", padx=4, pady=1
                )

        self._batch_job = self.after(0, self._render_next_batch)

    # ── Delete ────────────────────────────────────────────────────────

    def remove_employee(self, emp_id):
        def _do_delete():
            if delete_employee(emp_id):
                self.after(0, self.refresh_list)

        threading.Thread(target=_do_delete, daemon=True).start()

    # ── Add Employee Dialog ───────────────────────────────────────────

    def open_add_employee(self):
        win = ck.CTkToplevel(self)
        win.geometry("480x600")
        win.minsize(480, 600)
        win.title("Add Employee")
        win.attributes("-topmost", True)

        scroll = ck.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        form = ck.CTkFrame(scroll, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=20, pady=10)

        ck.CTkLabel(form, text="Add Employee",
                    font=("Serifa BT", 20, "bold"), text_color="#1b6a60").pack(anchor="w", pady=(0, 15))

        ck.CTkLabel(form, text="Full Name", font=("Serifa BT", 14)).pack(anchor="w")
        name_entry = ck.CTkEntry(form, placeholder_text="e.g. Dr. Sarah Banda", width=400)
        name_entry.pack(pady=(0, 10))

        ck.CTkLabel(form, text="Username", font=("Serifa BT", 14)).pack(anchor="w")
        username_entry = ck.CTkEntry(form, placeholder_text="e.g. sarah.banda", width=400)
        username_entry.pack(pady=(0, 10))

        ck.CTkLabel(form, text="Role", font=("Serifa BT", 14)).pack(anchor="w")
        role_var = ck.StringVar(value=ROLES[0])
        ck.CTkOptionMenu(form, variable=role_var, values=ROLES, width=400).pack(pady=(0, 10))

        ck.CTkLabel(form, text="Email", font=("Serifa BT", 14)).pack(anchor="w")
        email_entry = ck.CTkEntry(form, placeholder_text="email@hospital.com", width=400)
        email_entry.pack(pady=(0, 10))

        ck.CTkLabel(form, text="Phone", font=("Serifa BT", 14)).pack(anchor="w")
        phone_entry = ck.CTkEntry(form, placeholder_text="+260...", width=400)
        phone_entry.pack(pady=(0, 10))

        ck.CTkLabel(form, text="Password", font=("Serifa BT", 14)).pack(anchor="w")
        pass_entry = ck.CTkEntry(form, placeholder_text="••••••••", width=400, show="•")
        pass_entry.pack(pady=(0, 10))

        ck.CTkLabel(form, text="Confirm Password", font=("Serifa BT", 14)).pack(anchor="w")
        confirm_entry = ck.CTkEntry(form, placeholder_text="••••••••", width=400, show="•")
        confirm_entry.pack(pady=(0, 10))

        err_lbl = ck.CTkLabel(form, text="", text_color="#e74c3c", font=("Segoe UI", 11))
        err_lbl.pack(anchor="w")

        def submit():
            full_name = name_entry.get().strip()
            username  = username_entry.get().strip()
            role      = role_var.get()
            email     = email_entry.get().strip()
            phone     = phone_entry.get().strip()
            password  = pass_entry.get()
            confirm   = confirm_entry.get()

            if not all([full_name, username, email, phone, password]):
                err_lbl.configure(text="All fields are required.")
                return
            if password != confirm:
                err_lbl.configure(text="Passwords do not match.")
                return
            if len(password) < 6:
                err_lbl.configure(text="Password must be at least 6 characters.")
                return
            if email_exists(email):
                err_lbl.configure(text="An employee with this email already exists.")
                return

            def _do_save():
                ok = add_user(username, password, role, full_name, email, phone)
                if ok:
                    self.after(0, lambda: [win.destroy(), self.refresh_list()])
                else:
                    self.after(0, lambda: err_lbl.configure(text="Database error. Try again."))

            threading.Thread(target=_do_save, daemon=True).start()

        btn_row = ck.CTkFrame(form, fg_color="transparent")
        btn_row.pack(fill="x", pady=10)
        ck.CTkButton(btn_row, text="Cancel", fg_color="gray",
                     hover_color="#555", command=win.destroy
                     ).pack(side="left", expand=True, padx=5)
        ck.CTkButton(btn_row, text="Add Employee", fg_color="#1b6a60",
                     hover_color="#35988b", command=submit
                     ).pack(side="left", expand=True, padx=5)

    # ── Edit Employee Dialog ──────────────────────────────────────────

    def open_edit_employee(self, emp_id, data):
        # data: (emp_id, full_name, username, role, email, phone, created_at)
        win = ck.CTkToplevel(self)
        win.geometry("480x500")
        win.minsize(480, 500)
        win.title("Edit Employee")
        win.attributes("-topmost", True)

        scroll = ck.CTkScrollableFrame(win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        form = ck.CTkFrame(scroll, fg_color="transparent")
        form.pack(fill="both", expand=True, padx=20, pady=10)

        ck.CTkLabel(form, text="Edit Employee",
                    font=("Serifa BT", 20, "bold"), text_color="#1b6a60").pack(anchor="w", pady=(0, 15))

        def field(label, prefill):
            ck.CTkLabel(form, text=label, font=("Serifa BT", 14)).pack(anchor="w")
            e = ck.CTkEntry(form, width=400)
            e.insert(0, str(prefill) if prefill else "")
            e.pack(pady=(0, 10))
            return e

        name_entry     = field("Full Name", data[1])
        username_entry = field("Username",  data[2])

        ck.CTkLabel(form, text="Role", font=("Serifa BT", 14)).pack(anchor="w")
        role_var = ck.StringVar(value=data[3])
        ck.CTkOptionMenu(form, variable=role_var, values=ROLES, width=400).pack(pady=(0, 10))

        email_entry = field("Email", data[4])
        phone_entry = field("Phone", data[5])

        err_lbl = ck.CTkLabel(form, text="", text_color="#e74c3c", font=("Segoe UI", 11))
        err_lbl.pack(anchor="w")

        def submit():
            full_name = name_entry.get().strip()
            username  = username_entry.get().strip()
            role      = role_var.get()
            email     = email_entry.get().strip()
            phone     = phone_entry.get().strip()

            if not all([full_name, username, email, phone]):
                err_lbl.configure(text="All fields are required.")
                return

            def _do_update():
                ok = update_employee(emp_id, full_name, username, role, email, phone)
                if ok:
                    self.after(0, lambda: [win.destroy(), self.refresh_list()])
                else:
                    self.after(0, lambda: err_lbl.configure(text="Database error. Try again."))

            threading.Thread(target=_do_update, daemon=True).start()

        btn_row = ck.CTkFrame(form, fg_color="transparent")
        btn_row.pack(fill="x", pady=10)
        ck.CTkButton(btn_row, text="Cancel", fg_color="gray",
                     hover_color="#555", command=win.destroy
                     ).pack(side="left", expand=True, padx=5)
        ck.CTkButton(btn_row, text="Save Changes", fg_color="#1b6a60",
                     hover_color="#35988b", command=submit
                     ).pack(side="left", expand=True, padx=5)