import threading
import customtkinter as ck
from db_connector import get_all_patients, delete_patient, search_patients

COL_WEIGHTS = [1, 3, 1, 2, 3, 2, 1]  # ID, Name, Age, Contact, Symptoms, Billing, Actions
BATCH_SIZE  = 5


class PatientsPage(ck.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._row_pool: list[dict] = []
        self._pending_data: list   = []
        self._batch_job            = None
        self._fetch_thread         = None  # track live thread so we don't double-fetch

        # ── 1. Header & Search ────────────────────────────────────────
        self.HeaderFrame = ck.CTkFrame(self, fg_color="transparent")
        self.HeaderFrame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)

        ck.CTkLabel(
            self.HeaderFrame, text="Patient Directory",
            font=("Serifa BT", 28, "bold"), text_color="#1b6a60"
        ).pack(side="left")

        self.SearchEntry = ck.CTkEntry(
            self.HeaderFrame, placeholder_text="Search by Name...", width=300
        )
        self.SearchEntry.pack(side="right", padx=10)
        self.SearchEntry.bind("<Return>", lambda e: self.refresh_list())

        ck.CTkButton(
            self.HeaderFrame, text="Search", width=80,
            fg_color="#1b6a60", command=self.refresh_list
        ).pack(side="right")

        # ── 2. Table Header ───────────────────────────────────────────
        self.TableHeader = ck.CTkFrame(self, fg_color="#1b6a60", height=40, corner_radius=0)
        self.TableHeader.grid(row=1, column=0, sticky="ew", padx=20)

        for i, (name, w) in enumerate(zip(["ID","Name","Age","Contact","Symptoms","Billing","Actions"], COL_WEIGHTS)):
            self.TableHeader.grid_columnconfigure(i, weight=w)
            ck.CTkLabel(
                self.TableHeader, text=name,
                text_color="white", font=("Serifa BT", 13, "bold")
            ).grid(row=0, column=i, pady=5, sticky="ew")

        # ── 3. Loading label ──────────────────────────────────────────
        self.LoadingLabel = ck.CTkLabel(
            self, text="Loading patients...",
            font=("Segoe UI", 13), text_color="#888888"
        )
        self.LoadingLabel.grid(row=2, column=0, pady=40)

        # ── 4. Scrollable list ────────────────────────────────────────
        self.ListArea = ck.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        for i, weight in enumerate(COL_WEIGHTS):
            self.ListArea.grid_columnconfigure(i, weight=weight)

        self.after(50, self.refresh_list)

    # ── Row pool ──────────────────────────────────────────────────────

    def _get_row(self, index: int) -> dict:
        if index < len(self._row_pool):
            return self._row_pool[index]

        frame = ck.CTkFrame(self.ListArea, fg_color="#f9f9f9", height=35, corner_radius=4)
        for i, weight in enumerate(COL_WEIGHTS):
            frame.grid_columnconfigure(i, weight=weight)

        labels = []
        for col in range(6):  # ID, Name, Age, Contact, Symptoms, Billing
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

    # ── Refresh entry point (always called from main thread) ──────────

    def refresh_list(self):
        # Cancel any in-progress batch render
        if self._batch_job is not None:
            self.after_cancel(self._batch_job)
            self._batch_job = None

        # Don't spin up a second fetch if one is already running
        if self._fetch_thread and self._fetch_thread.is_alive():
            return

        self.ListArea.grid_remove()
        self.LoadingLabel.grid(row=2, column=0, pady=40)
        self.LoadingLabel.configure(text="Loading patients...")

        search_term = self.SearchEntry.get().strip()

        # ── Run DB query on a background thread ───────────────────────
        # RULE: never touch tkinter widgets inside _do_fetch.
        #       Only call self.after() to hand results back to main thread.
        def _do_fetch():
            try:
                data = search_patients(search_term) if search_term else get_all_patients()
            except Exception as e:
                data = []
                print(f"Fetch error: {e}")
            # Hand results back to the main thread safely
            self.after(0, lambda: self._on_fetch_complete(data))

        self._fetch_thread = threading.Thread(target=_do_fetch, daemon=True)
        self._fetch_thread.start()

    # ── Called on main thread once DB responds ────────────────────────

    def _on_fetch_complete(self, data: list):
        if not data:
            self.LoadingLabel.configure(text="No patients found.")
            for row in self._row_pool:
                if row["frame"].winfo_ismapped():
                    row["frame"].grid_remove()
            return

        # Hide rows beyond the new result count
        for i in range(len(data), len(self._row_pool)):
            row = self._row_pool[i]
            if row["frame"].winfo_ismapped():
                row["frame"].grid_remove()

        self._pending_data = list(enumerate(data))
        self._render_next_batch()

    # ── Batched rendering (main thread, non-blocking) ─────────────────

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
            p_id = item[0]
            row  = self._get_row(i)

            for col_idx, value in enumerate(item):
                row["labels"][col_idx].configure(text=str(value))

            row["btn"].configure(command=lambda pid=p_id: self.remove_patient(pid))

            if not row["frame"].winfo_ismapped():
                row["frame"].grid(
                    row=i, column=0, columnspan=len(COL_WEIGHTS),
                    sticky="ew", padx=4, pady=1
                )

        self._batch_job = self.after(0, self._render_next_batch)

    # ── Delete ────────────────────────────────────────────────────────

    def remove_patient(self, p_id):
        # Delete also runs on a background thread so the UI doesn't hitch
        def _do_delete():
            success = delete_patient(p_id)
            if success:
                self.after(0, self.refresh_list)

        threading.Thread(target=_do_delete, daemon=True).start()