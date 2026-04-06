import customtkinter as ck
from PIL import Image
import os 
from tkinter import filedialog
from PatientsPage import PatientsPage
from AppointmentsPage import AppointmentsPage
from PaymentsPage import PaymentsPage
from EmployeePage import EmployeePage
from db_connector import (
    save_patient, get_dashboard_stats,
    get_upcoming_appointments, get_payment_summary
)


PATH = os.path.dirname(os.path.realpath(__file__))


class AdminPanelFrame(ck.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        
#------------------------------Images---------------------------------------------------------------------------------------#
               
        all_img_paths = [
        "assets/Dashboard.png",
        "assets/patients.png",
        "assets/appointment.png",
        "assets/payment.png",
        "assets/employee.png",
        "assets/activity.png",
        "assets/help.png",
        "assets/settings.png",
        "assets/flag.png",
        "assets/logout.png",
        "assets/search.png",
        "assets/user.png",
        "assets/doctor.png",
        "assets/bed.png",
    ]

        # Open each file exactly once, store as CTkImage
        loaded = []
        for p in all_img_paths:
            img = Image.open(p)
            loaded.append(ck.CTkImage(light_image=img, dark_image=img, size=(15,15)))

        self.all_icons  = loaded[0:6]   # sidebar main buttons
        self.all_others = loaded[6:9]   # sidebar other buttons
        self.logout_img = loaded[9]
        self.search_icon = loaded[10]
        self.user_logo   = loaded[11]
        self.doc_icon    = loaded[12]
        self.bed_icon    = loaded[13]

        # appointment.png is already in loaded[2], reuse it instead of loading again
        self.appt_icon = loaded[2]

        
        self.Widgets()

    def logout_func(self):
        self.master.show_login()
    
    
    def add_patient(self):
        window = ck.CTkToplevel(self)
        window.geometry("500x700") 
        window.title("Add Patient")
        window.attributes("-topmost", True) 

        # --- Form Container ---
        form_frame = ck.CTkFrame(window, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # 1. Full Name
        ck.CTkLabel(form_frame, text="Full Name", font=("Serifa BT", 14)).pack(anchor="w")
        name_entry = ck.CTkEntry(form_frame, placeholder_text="e.g. Maron Chilomo", width=400)
        name_entry.pack(pady=(0, 10))

        # 2. Age & Contact (Side by Side)
        row2 = ck.CTkFrame(form_frame, fg_color="transparent")
        row2.pack(fill="x", pady=(0, 10))
        
        age_entry = ck.CTkEntry(row2, placeholder_text="Age", width=80)
        age_entry.pack(side="left", padx=(0, 10))
        
        contact_entry = ck.CTkEntry(row2, placeholder_text="Phone Number", width=310)
        contact_entry.pack(side="left")

        # 3. Address & Email
        ck.CTkLabel(form_frame, text="Email Address", font=("Serifa BT", 14)).pack(anchor="w")
        email_entry = ck.CTkEntry(form_frame, placeholder_text="example@gmail.com", width=400)
        email_entry.pack(pady=(0, 10))

        ck.CTkLabel(form_frame, text="Residential Address", font=("Serifa BT", 14)).pack(anchor="w")
        address_entry = ck.CTkEntry(form_frame, placeholder_text="e.g. Avondale, Lusaka", width=400)
        address_entry.pack(pady=(0, 10))

        # 4. Symptoms / Experience (Textbox)
        ck.CTkLabel(form_frame, text="Symptoms / Experience", font=("Serifa BT", 14)).pack(anchor="w")
        symptoms_text = ck.CTkTextbox(form_frame, height=100, width=400, border_width=2)
        symptoms_text.pack(pady=(0, 15))

        # 5. Service Type (Radio Buttons)
        ck.CTkLabel(form_frame, text="Service Billing", font=("Serifa BT", 14, "bold")).pack(anchor="w")
        billing_var = ck.StringVar(value="Paid") # Default value
        
        radio_row = ck.CTkFrame(form_frame, fg_color="transparent")
        radio_row.pack(fill="x", pady=5)
        
        paid_rb = ck.CTkRadioButton(radio_row, text="Paid Service", variable=billing_var, value="Paid", fg_color="#1b6a60")
        paid_rb.pack(side="left", padx=(0, 20))
        
        free_rb = ck.CTkRadioButton(radio_row, text="Free Service", variable=billing_var, value="Free", fg_color="#1b6a60")
        free_rb.pack(side="left")

        # --- Backend Logic Functions ---
        def send_to_database():
            # Get the data from entries
            name = name_entry.get()
            age = age_entry.get()
            contact = contact_entry.get()
            email = email_entry.get()
            address = address_entry.get()
            symptoms = symptoms_text.get("1.0", "end-1c") # Gets all text from textbox
            billing = billing_var.get()

            # Input validation (Basic check)
            if not name or not age or not contact:
                print("Error: Name, Age, and Contact are required.")
                return

            # Call the function from db_connector.py
            if save_patient(name, age, contact, email, address, symptoms, billing):
                print(f"Success: {name} added to database.")
                # Refresh the PatientsPage table automatically
                if hasattr(self, 'Patients_Container'):
                    self.Patients_Container.refresh_list()
                window.destroy() 
            else:
                print("Database Error: Could not save patient.")

        def clear_form():
            name_entry.delete(0, 'end')
            age_entry.delete(0, 'end')
            contact_entry.delete(0, 'end')
            email_entry.delete(0, 'end')
            address_entry.delete(0, 'end')
            symptoms_text.delete("1.0", 'end')
            billing_var.set("Paid")

        # --- Action Buttons ---
        btn_row = ck.CTkFrame(form_frame, fg_color="transparent")
        btn_row.pack(fill="x", pady=20)

        clear_btn = ck.CTkButton(btn_row, text="Clear Form", fg_color="gray", 
                                 hover_color="#952321", command=clear_form)
        clear_btn.pack(side="left", padx=5, expand=True)

        book_btn = ck.CTkButton(btn_row, text="Book Appointment", fg_color="#1b6a60", 
                                hover_color="#35988b", command=send_to_database)
        book_btn.pack(side="left", padx=5, expand=True)
        
        
        
    
    #//MIGHT USE THIS AS THE NEXT RENDER ENGINE.
    # def render_image(self):
    #     image_paths = [ ]

    #     self.new_paths = [ ]
        
    #     for img in image_paths:
    #         pic = Image.open(img)
    #         self.pic = ck.CTkImage(light_image=pic, dark_image=pic, size=(15,15))
    #         self.new_paths.append(self.pic)
            
            

    def change_profile_pic(self):
        selected_file_path = filedialog.askopenfilename(
            title= "Select Profile Picture",
            initialdir= "/home/mrr_whoo/Downloads",
            filetypes= [("Image files", "*.png *.jpg *.jpeg")]
            )
        if selected_file_path:
            print(f"User selected: {selected_file_path}")
            
            new_image = Image.open(selected_file_path)
            self.ProfileIcon = ck.CTkImage(light_image=new_image,dark_image=new_image,size=(20,20))
            # self.ProfileLabel.configure(imgage = self.ProfileIcon)
            
            
    def hide_dashboard(self):
        self.DashBoard_Container.pack_forget()

    def show_patients(self):
        self.DashBoard_Container.pack_forget()
        self.Appt_Container.pack_forget()
        self.Payments_Container.pack_forget()
        self.Employee_Container.pack_forget()
        self.Patients_Container.pack(fill="both", expand=True)

    def show_dashboard(self):
        self.Patients_Container.pack_forget()
        self.Appt_Container.pack_forget()
        self.Payments_Container.pack_forget()
        self.Employee_Container.pack_forget()
        self.DashBoard_Container.pack(fill="both", expand=True)

    def show_appointments(self):
        self.Patients_Container.pack_forget()
        self.DashBoard_Container.pack_forget()
        self.Payments_Container.pack_forget()
        self.Employee_Container.pack_forget()
        self.Appt_Container.pack(fill="both", expand=True)

    def show_payments(self):
        self.Patients_Container.pack_forget()
        self.DashBoard_Container.pack_forget()
        self.Appt_Container.pack_forget()
        self.Employee_Container.pack_forget()
        self.Payments_Container.pack(fill="both", expand=True)

    def show_employees(self):
        self.Patients_Container.pack_forget()
        self.DashBoard_Container.pack_forget()
        self.Appt_Container.pack_forget()
        self.Payments_Container.pack_forget()
        self.Employee_Container.pack(fill="both", expand=True)
    
    def _load_dashboard(self):
        """Fetch all dashboard data on a background thread."""
        import threading
        def _fetch():
            stats   = get_dashboard_stats()
            appts   = get_upcoming_appointments(limit=5)
            payment = get_payment_summary()
            self.after(0, lambda: self._apply_dashboard(stats, appts, payment))
        threading.Thread(target=_fetch, daemon=True).start()

    def refresh_dashboard(self):
        """Call this whenever data changes to re-sync the dashboard."""
        self._load_dashboard()

    def _apply_dashboard(self, stats, appts, payment):
        # ── Stat cards ────────────────────────────────────────────────
        values = {
            "patients":     str(stats.get("total_patients", 0)),
            "appointments": str(stats.get("total_appointments", 0)),
            "doctors":      str(stats.get("total_doctors", 0)),
            "revenue":      f"K {payment.get('total_revenue', 0):,.0f}",
        }
        for key, (btn, title) in self._stat_btns.items():
            btn.configure(text=f"{title}\n{values[key]}")

        # ── Upcoming Appointments ─────────────────────────────────────
        for w in self.ApptListFrame.winfo_children():
            w.destroy()
        if not appts:
            ck.CTkLabel(self.ApptListFrame, text="No upcoming appointments",
                        text_color="#a8d8d4", font=("Segoe UI", 11)
                        ).grid(row=0, column=0, pady=15)
        else:
            for i, appt in enumerate(appts):
                _, appt_time, patient, doctor, dept, status = appt
                row_bg = "#17574f" if i % 2 == 0 else "#1b6a60"
                row = ck.CTkFrame(self.ApptListFrame, fg_color=row_bg, corner_radius=6)
                row.grid(row=i, column=0, sticky="ew", pady=2)
                row.grid_columnconfigure(1, weight=1)
                ck.CTkLabel(row, text=str(appt_time)[:16], font=("Segoe UI", 10, "bold"),
                            text_color="#a8f0e8", width=120, anchor="w"
                            ).grid(row=0, column=0, padx=(8, 4), pady=5, sticky="w")
                ck.CTkLabel(row, text=f"{patient}  ·  Dr. {doctor}",
                            font=("Segoe UI", 11), text_color="white", anchor="w"
                            ).grid(row=0, column=1, sticky="ew", padx=4)
                pill = "#2ecc71" if status == "Confirmed" else "#e67e22" if status == "Pending" else "#95a5a6"
                ck.CTkLabel(row, text=status, font=("Segoe UI", 10), text_color="white",
                            fg_color=pill, corner_radius=8, width=65
                            ).grid(row=0, column=2, padx=(4, 8), pady=5)

        # ── Patient Statistics ────────────────────────────────────────
        for w in self.PatientStatsFrame.winfo_children():
            w.destroy()
        paid_count = stats.get("paid_patients", 0)
        free_count = stats.get("free_patients", 0)
        total      = paid_count + free_count or 1
        stat_rows  = [
            ("Total Patients",  stats.get("total_patients", 0),   "#51c4b5"),
            ("Paid Billing",    paid_count,                        "#2ecc71"),
            ("Free Billing",    free_count,                        "#e67e22"),
            ("Appointments",    stats.get("total_appointments", 0),"#3498db"),
        ]
        for i, (label, val, color) in enumerate(stat_rows):
            r = ck.CTkFrame(self.PatientStatsFrame, fg_color="#17574f", corner_radius=6)
            r.grid(row=i, column=0, sticky="ew", pady=2, padx=2)
            r.grid_columnconfigure(1, weight=1)
            ck.CTkLabel(r, text=label, font=("Segoe UI", 11),
                        text_color="white", anchor="w"
                        ).grid(row=0, column=0, padx=10, pady=6, sticky="w")
            ck.CTkLabel(r, text=str(val), font=("Segoe UI", 13, "bold"),
                        text_color=color, anchor="e"
                        ).grid(row=0, column=1, padx=10, pady=6, sticky="e")

        # ── Doctor Availability ───────────────────────────────────────
        for w in self.DocAvailFrame.winfo_children():
            w.destroy()
        doctors = stats.get("doctors_list", [])
        if not doctors:
            ck.CTkLabel(self.DocAvailFrame, text="No doctors found",
                        text_color="#a8d8d4", font=("Segoe UI", 11)
                        ).grid(row=0, column=0, pady=15)
        else:
            for i, (name, status) in enumerate(doctors):
                row_bg = "#17574f" if i % 2 == 0 else "#1b6a60"
                r = ck.CTkFrame(self.DocAvailFrame, fg_color=row_bg, corner_radius=6)
                r.grid(row=i, column=0, sticky="ew", pady=2)
                r.grid_columnconfigure(0, weight=1)
                ck.CTkLabel(r, text=name, font=("Segoe UI", 11),
                            text_color="white", anchor="w"
                            ).grid(row=0, column=0, padx=10, pady=6, sticky="w")
                pill = "#2ecc71" if status == "Active" else "#e74c3c"
                ck.CTkLabel(r, text=status, font=("Segoe UI", 10),
                            text_color="white", fg_color=pill,
                            corner_radius=8, width=55
                            ).grid(row=0, column=1, padx=(4, 8), pady=6)

        # ── Payment Summary ───────────────────────────────────────────
        for w in self.PaySummaryFrame.winfo_children():
            w.destroy()
        pay_rows = [
            ("Total Revenue",  f"K {payment.get('total_revenue', 0):,.2f}", "#2ecc71"),
            ("Paid",           str(payment.get("paid_count", 0)),            "#2ecc71"),
            ("Pending",        str(payment.get("pending_count", 0)),         "#e67e22"),
            ("Overdue",        str(payment.get("overdue_count", 0)),         "#e74c3c"),
        ]
        for i, (label, val, color) in enumerate(pay_rows):
            r = ck.CTkFrame(self.PaySummaryFrame, fg_color="#17574f", corner_radius=6)
            r.grid(row=i, column=0, sticky="ew", pady=2, padx=2)
            r.grid_columnconfigure(1, weight=1)
            ck.CTkLabel(r, text=label, font=("Segoe UI", 11),
                        text_color="white", anchor="w"
                        ).grid(row=0, column=0, padx=10, pady=6, sticky="w")
            ck.CTkLabel(r, text=val, font=("Segoe UI", 13, "bold"),
                        text_color=color, anchor="e"
                        ).grid(row=0, column=1, padx=10, pady=6, sticky="e")

    def Widgets(self):
#------------------------------------CONTAINERS SETUP-----------------------------------------------------------------------
        # MAIN CONTAINER - The base for everything
        self.MainContainer = ck.CTkFrame(self, fg_color="transparent")
        self.MainContainer.pack(fill="both", expand=True)

        # SIDEBAR - Fixed to the left
        self.SideBarFrame = ck.CTkFrame(self.MainContainer, fg_color="#1b6a60", corner_radius=5, width=200)
        self.SideBarFrame.pack(side="left", fill="y")
        
        # CONTENT AREA - The "Viewing Window" on the right
        self.ContentFrame = ck.CTkFrame(self.MainContainer, fg_color="white")
        self.ContentFrame.pack(side="right", fill="both", expand=True)

        # DASHBOARD CONTAINER - Resides inside ContentArea
        self.DashBoard_Container = ck.CTkFrame(self.ContentFrame, fg_color="white")
        self.DashBoard_Container.pack(fill="both", expand=True)

        # PATIENTS CONTAINER - Also resides inside ContentArea (Initially hidden)
        self.Patients_Container = PatientsPage(self.ContentFrame, fg_color="white")
        
        self.Appt_Container = AppointmentsPage(self.ContentFrame, fg_color="white")

        self.Payments_Container = PaymentsPage(self.ContentFrame, fg_color="white")
        self.Employee_Container = EmployeePage(self.ContentFrame, fg_color="white")

#------------------------------------SIDEBAR BUTTONS------------------------------------------------------------------------
        self.MedCare = ck.CTkLabel(self.SideBarFrame, text="🏥 MedCare", font=("Times new roman", 30, "bold"))
        self.MedCare.pack(pady=(8, 25))
        
        self.menu = ck.CTkLabel(self.SideBarFrame, text="MENU", font=("Herald", 10))
        self.menu.pack(anchor="w", padx=20)
        
        SideButtons = ['Dashboard', 'Patients', 'Appointments', 'Payments', 'Employee', 'Activity']
        
        for but, icon in zip(SideButtons, self.all_icons):
            if but == "Dashboard":
                command = self.show_dashboard
            elif but == "Patients":
                command = self.show_patients  
            elif but == "Appointments": 
                command = self.show_appointments
            elif but == "Payments":
                command = self.show_payments
            elif but == "Employee":
                command = self.show_employees
            else:
                command = None  

            ck.CTkButton(
                self.SideBarFrame,
                text=but,
                image=icon,
                width=300,
                height=40,
                compound="left",
                font=("Serifa BT", 15),
                anchor="w",
                fg_color="#1b6a60",
                hover_color="#2a8a7e",
                command=command
            ).pack(pady=(1, 3))
        
        self.othermenu = ck.CTkLabel(self.SideBarFrame, text="OTHER MENU", font=("Herald", 10))
        self.othermenu.pack(anchor="w", padx=20)
            
        self.MoreButtons = ['Help & Center', 'Settings', 'Report']
        for but, icon in zip(self.MoreButtons, self.all_others):
            ck.CTkButton(self.SideBarFrame, text=but, image=icon, width=300, height=40, anchor="w", 
                         font=("Serifa BT", 15), fg_color="#1b6a60", hover_color="gray").pack(pady=(1, 3))
            
        self.logout = ck.CTkButton(self.SideBarFrame, command=self.logout_func, text="Logout", width=280, 
                                   height=40, image=self.logout_img, anchor="w", hover_color="#3ea294", 
                                   fg_color="#1b6a60", corner_radius=20)
        self.logout.pack(pady=(430, 10), side="left", padx=3) # Changed to side="bottom" for better alignment

#-------------------------------DASHBOARD CONTENT WIDGETS-------------------------------------------------------------------
        # Search Bar
        self.SearchBarFrame = ck.CTkFrame(self.DashBoard_Container, fg_color="white")
        self.SearchBarFrame.pack(side="top", fill="x")
        
        self.SearchButton = ck.CTkButton(self.SearchBarFrame, image=self.search_icon, fg_color="white", height=30, 
                                         compound="left", text_color="gray", text="search here", 
                                         hover_color="white", font=("Serifa BT", 23), command=self.show_patients)
        self.SearchButton.pack(side="left", expand=True, fill="x")
        
        self.AddPatient = ck.CTkButton(self.SearchBarFrame, text="Add Patient", font=("Serifa BT", 20), 
                                       fg_color="#1b6a60", corner_radius=10, hover_color="#35988b", 
                                       command=self.add_patient)
        self.AddPatient.pack(side="left", padx=3)

        self.hellolabel = ck.CTkLabel(self.DashBoard_Container, text="Hello, Default", font=("Serifa BT", 20))
        self.hellolabel.pack(anchor="w", padx=10, pady=(1, 1))

        # ── Stats Cards ───────────────────────────────────────────────
        self.StatsContainer = ck.CTkFrame(self.DashBoard_Container, fg_color="white")
        self.StatsContainer.pack(fill="x", padx=20, pady=7)

        stats_defs = [
            ("Total Patients", "—", self.user_logo,  "patients"),
            ("Appointments",   "—", self.appt_icon,  "appointments"),
            ("Doctors",        "—", self.doc_icon,   "doctors"),
            ("Total Revenue",  "—", self.bed_icon,   "revenue"),
        ]
        self._stat_btns = {}
        for title, val, icon, key in stats_defs:
            f = ck.CTkFrame(self.StatsContainer, corner_radius=15, fg_color="#51c4b5")
            f.pack(side="left", fill="both", expand=True, padx=5)
            btn = ck.CTkButton(f, text=f"{title}\n{val}", image=icon, compound="top",
                               font=("Serifa BT", 18), fg_color="#51c4b5",
                               text_color="black", hover_color="#51c4b5", height=150)
            btn.pack(pady=10, fill="both", expand=True)
            self._stat_btns[key] = (btn, title)

        # ── Grid Section ──────────────────────────────────────────────
        self.GridContainer = ck.CTkFrame(self.DashBoard_Container, fg_color="transparent")
        self.GridContainer.pack(fill="both", expand=True, padx=20, pady=0)
        self.GridContainer.columnconfigure((0, 1), weight=1, uniform="equal")
        self.GridContainer.rowconfigure((0, 1), weight=1, uniform="equal")

        # ── [0,0] Upcoming Appointments ───────────────────────────────
        appt_card = ck.CTkFrame(self.GridContainer, corner_radius=15, fg_color="#1b6a60")
        appt_card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        appt_card.grid_rowconfigure(1, weight=1)
        appt_card.grid_columnconfigure(0, weight=1)
        ck.CTkLabel(appt_card, text="📅 Upcoming Appointments",
                    font=("Serifa BT", 18, "bold"), text_color="white"
                    ).grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))
        self.ApptListFrame = ck.CTkFrame(appt_card, fg_color="transparent")
        self.ApptListFrame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 10))
        self.ApptListFrame.grid_columnconfigure(0, weight=1)

        # ── [0,1] Patient Statistics ──────────────────────────────────
        stats_card = ck.CTkFrame(self.GridContainer, corner_radius=15, fg_color="#1b6a60")
        stats_card.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        stats_card.grid_rowconfigure(1, weight=1)
        stats_card.grid_columnconfigure(0, weight=1)
        ck.CTkLabel(stats_card, text="📊 Patient Statistics",
                    font=("Serifa BT", 18, "bold"), text_color="white"
                    ).grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))
        self.PatientStatsFrame = ck.CTkFrame(stats_card, fg_color="transparent")
        self.PatientStatsFrame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 10))
        self.PatientStatsFrame.grid_columnconfigure(0, weight=1)

        # ── [1,0] Doctor Availability ─────────────────────────────────
        doc_card = ck.CTkFrame(self.GridContainer, corner_radius=15, fg_color="#1b6a60")
        doc_card.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        doc_card.grid_rowconfigure(1, weight=1)
        doc_card.grid_columnconfigure(0, weight=1)
        ck.CTkLabel(doc_card, text="👨‍⚕️ Doctor Availability",
                    font=("Serifa BT", 18, "bold"), text_color="white"
                    ).grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))
        self.DocAvailFrame = ck.CTkFrame(doc_card, fg_color="transparent")
        self.DocAvailFrame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 10))
        self.DocAvailFrame.grid_columnconfigure(0, weight=1)

        # ── [1,1] Payment Summary ─────────────────────────────────────
        pay_card = ck.CTkFrame(self.GridContainer, corner_radius=15, fg_color="#1b6a60")
        pay_card.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        pay_card.grid_rowconfigure(1, weight=1)
        pay_card.grid_columnconfigure(0, weight=1)
        ck.CTkLabel(pay_card, text="💰 Payment Summary",
                    font=("Serifa BT", 18, "bold"), text_color="white"
                    ).grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))
        self.PaySummaryFrame = ck.CTkFrame(pay_card, fg_color="transparent")
        self.PaySummaryFrame.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 10))
        self.PaySummaryFrame.grid_columnconfigure(0, weight=1)

        # Kick off live data load after window renders
        self.after(100, self._load_dashboard)