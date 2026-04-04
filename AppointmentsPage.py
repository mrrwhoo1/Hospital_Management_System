import customtkinter as ck
from db_connector import save_appointment, get_all_appointments, delete_appointment

class AppointmentsPage(ck.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Header
        self.Header = ck.CTkFrame(self, fg_color="transparent")
        self.Header.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        
        ck.CTkLabel(self.Header, text="Hospital Appointments", 
                    font=("Serifa BT", 28, "bold"), text_color="#1b6a60").pack(side="left")
        
        self.AddApptBtn = ck.CTkButton(self.Header, text="+ Schedule New", 
                                       fg_color="#1b6a60", hover_color="#2a8a7e",
                                       command=self.open_add_appointment_window)
        self.AddApptBtn.pack(side="right", padx=10)

        # Table Header
        self.TableHeader = ck.CTkFrame(self, fg_color="#1b6a60", height=40, corner_radius=0)
        self.TableHeader.grid(row=1, column=0, sticky="ew", padx=20)
        
        cols = ["Time", "Patient Name", "Doctor", "Department", "Status"]
        for i, name in enumerate(cols):
            self.TableHeader.grid_columnconfigure(i, weight=1)
            ck.CTkLabel(self.TableHeader, text=name, text_color="white", 
                        font=("Serifa BT", 13, "bold")).grid(row=0, column=i, pady=5)

        # Scrollable List Area
        self.ListArea = ck.CTkScrollableFrame(self, fg_color="transparent", corner_radius=0)
        self.ListArea.grid(row=2, column=0, sticky="nsew", padx=20, pady=(10, 20))
        
        self.refresh_list()

    def refresh_list(self):
        """Fetches REAL data and adds a Delete button to each row"""
        for widget in self.ListArea.winfo_children():
            widget.destroy()
            
        # Update the SQL query in db_connector to include appt_id:
        # "SELECT appt_id, appt_time, patient_name, doctor_name, department, status FROM appointments"
        data = get_all_appointments() 
        
        for item in data:
            appt_id = item[0]  # The ID from the database
            row = ck.CTkFrame(self.ListArea, fg_color="#f9f9f9", height=40)
            row.pack(fill="x", pady=2)
            
            # Display data columns (Time, Patient, etc.)
            for i in range(1, len(item)):
                row.grid_columnconfigure(i, weight=1)
                ck.CTkLabel(row, text=str(item[i]), text_color="black").grid(row=0, column=i)

            # Add the Delete Button at the end of the row
            delete_btn = ck.CTkButton(
                row, 
                text="Delete", 
                width=60, 
                height=25, 
                fg_color="#952321", 
                hover_color="#701a18",
                command=lambda id=appt_id: self.confirm_delete(id)
            )
            delete_btn.grid(row=0, column=len(item), padx=10)

    def confirm_delete(self, appt_id):
            # Call the database function
        if delete_appointment(appt_id):
            self.refresh_list() # Refresh UI to show the row is gone
        else:
            print("Failed to delete.")

    def open_add_appointment_window(self):
        window = ck.CTkToplevel(self)
        window.geometry("400x500")
        window.title("Schedule Appointment")
        window.attributes("-topmost", True)

        # Form Fields
        ck.CTkLabel(window, text="Patient Name").pack(pady=(20, 0))
        name_entry = ck.CTkEntry(window, width=250)
        name_entry.pack()

        ck.CTkLabel(window, text="Doctor Name").pack(pady=(10, 0))
        doc_entry = ck.CTkEntry(window, width=250)
        doc_entry.pack()

        ck.CTkLabel(window, text="Department").pack(pady=(10, 0))
        dept_cb = ck.CTkComboBox(window, values=["General", "Dental", "Optical", "Surgical"], width=250)
        dept_cb.pack()

        ck.CTkLabel(window, text="Time (e.g. 10:30 AM)").pack(pady=(10, 0))
        time_entry = ck.CTkEntry(window, width=250)
        time_entry.pack()

        def save_logic():
            if save_appointment(name_entry.get(), doc_entry.get(), dept_cb.get(), time_entry.get()):
                self.refresh_list() # Immediately show the new record
                window.destroy()
            else:
                print("Database save failed.")

        ck.CTkButton(window, text="Save to Database", fg_color="#1b6a60", 
                     command=save_logic).pack(pady=30)