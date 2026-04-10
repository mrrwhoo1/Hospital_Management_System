import random
from db_connector         import add_user, email_exists

def add_employees():
    roles = ['Admin','Physiotherapist','Pharmacist','Receptionist','Doctor','Janitor','Security','Nurse']
    weights = [1,10,10,20,30,30,30,40]
    
    with open("assets/employee_names.txt", "r") as employees:
        lines = employees.readlines()
        for indexx, name in enumerate(lines, start = 1):
            username = name.strip().lower().replace(" ","_")
            default_password = name.strip().lower().replace(" ", "") + "1234"
            role = random.choices(roles, weights=weights,k=1)[0]
            name = name.strip()
            email = name.strip().replace(" ","").lower() + "@gmail.com"
            #-----------------------------phone number logic----------------------
            phone_prefixes = ["97","96","95","77", "76"]
            prefix = random.choice(phone_prefixes)
            digits = "".join(random.choices('0123456789', k = 7))
            phone = f"+260{prefix}{digits}"
            
            if not email_exists(email):
                if email == "maronchilomo@gmail.com":
                    username = "mrr_whoo"
                    default_password = "fodavoce"
                    role = "Admin"
                add_user(username,default_password,role,name,email,phone)
                print(f'Added{indexx}. {username} with role "{role}".')
            else:
                print(f"{indexx}. Skipped: {name} (Already in database)")
                
add_employees()
        
       
        
        
            
            
        
        

            
    
