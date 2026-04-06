import customtkinter as ck
import platform
import os
from PIL import Image
from db_connector import db_connect_verifyer
from CTkMessagebox import CTkMessagebox
from AdminPanel import AdminPanelFrame



ck.set_appearance_mode("system")
PATH = os.path.dirname(os.path.realpath(__file__))

class HealthApp(ck.CTk):
    def __init__(self):
        super().__init__()
        
        
        self.title("Health Management System")
        self.window_maximizer()
        self.resizable(False, False)

        bg_path = os.path.join(PATH, "assets/background.png")
        bg_img = Image.open(bg_path)
        self.bg_image = ck.CTkImage(light_image=bg_img, dark_image=bg_img,
                                    size=(self.winfo_screenwidth(), self.winfo_screenheight()))

        logo_path = os.path.join(PATH, "assets/hospital_logo.png")
        logo_img = Image.open(logo_path)
        self.hp_logo = ck.CTkImage(light_image=logo_img, dark_image=logo_img, size=(200, 150))

        self.login_page = ck.CTkLabel(self, image=self.bg_image, text="")

        # self.setup_login_ui()
        # self.show_login()
        #this is a place holder that i used for testing
        #NOTE: FOR ALL THAT WILL EVER RUN THIS, AFTER YOU MAKE THE DB UNCOMMENT OUT THE 2 ABOVE FUNCTIONS AND COMMENT OUT SHOW DASHBOARD! THANKS.
        self.show_dashboard(name = "mrr_whoo", role = "Admin") 
    
    def setup_login_ui(self):
        """Builds the login box directly on top of the background label"""
        self.login_box = ck.CTkFrame(self.login_page, fg_color="white",bg_color = "white" , corner_radius=40)
        self.login_box.place(relx=0.65, rely=0.45, anchor="w")
        
        self.hospital_label = ck.CTkLabel(self.login_box, image=self.hp_logo, compound="top",
                                          text="Hospital Support System", font=("Ariel", 30), text_color="Black")
        self.hospital_label.pack(pady=(1, 100), padx=65)

        self.login_entry_user = ck.CTkEntry(self.login_box, placeholder_text="username", 
                                            fg_color="light gray", font=("Ariel", 20), width=300, height=40, 
                                            corner_radius=20, text_color="Black")
        self.login_entry_user.pack(pady=(10, 15), padx=10)

        self.login_entry_pass = ck.CTkEntry(self.login_box, placeholder_text="password", 
                                            fg_color="light gray", font=("Ariel", 20), width=300, height=40, 
                                            corner_radius=20, text_color="black", show="*")
        self.login_entry_pass.pack(pady=1, padx=10)

        self.forgot_password_button = ck.CTkButton(self.login_box, text = "Forgot password", fg_color = "white", text_color="gray", hover_color= "white")
        self.forgot_password_button.pack(pady = 5)
        
        self.LoginButton = ck.CTkButton(self.login_box, text="Login", width=150, command=self.on_login_click)
        self.LoginButton.pack(pady=20)

    
    def show_login(self):
        if hasattr(self, 'AdminPage'):
            self.AdminPage.pack_forget()
        self.login_page.pack(fill="both", expand=True)

    def show_dashboard(self, name, role):
        self.login_page.pack_forget()
        if not hasattr(self, 'AdminPage'):
            self.AdminPage = AdminPanelFrame(self, fg_color="#F2F2F2")
        self.AdminPage.pack(fill="both", expand=True)

 
    def on_login_click(self):
        u = self.login_entry_user.get()
        p = self.login_entry_pass.get()
        data = db_connect_verifyer(u, p)
        
        if data:
            role, fullName = data
            
            self.login_entry_user.delete(0, 'end')
            self.login_entry_pass.delete(0, 'end')
            # Trigger the switch
            self.show_dashboard(fullName, role)
            

            
        else:
            CTkMessagebox(title="Access Denied", message="Invalid credentials", icon="cancel", corner_radius=20)

    
    #Func to decide window width
    def window_maximizer(window):

        os_name = platform.system()

        try:
            if os_name == "Windows":
                window.state("zoomed")

            elif os_name == "Linux":
               window.attributes('zoomed', True)
            else:
                window.state("zoomed")

        except Exception:
            width = window.winfo_screenwidth()
            height = window.winfo_screenheight()
            window.geometry(f"{width}x{height}+0+0")

if __name__ == "__main__":
    app = HealthApp()
    app.mainloop()