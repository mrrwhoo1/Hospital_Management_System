import random
from db_connector import save_patient, patient_exists

def add_patients_batch():
    # Lusaka areas for realistic addresses
    areas = ["Avondale", "Chilenje", "Woodlands", "Madina", "Chelstone", "Kabwe Road", "Rhodes Park"]
    
    # Path to your uploaded txt file
    file_path = "assets/patient_names_newlines.txt"

    try:
        with open(file_path, "r") as patients_file:
            lines = patients_file.readlines()
            
            for index, name in enumerate(lines, start=1):
                name = name.strip()
                if not name:
                    continue
                
                # --- Random Data Generation ---
                age = random.randint(1, 90)
                email = name.lower().replace(" ", "") + "@gmail.com"
                address = f"{random.randint(1, 200)} {random.choice(areas)}, Lusaka"
                symptoms = random.choice(["Headache", "Fever", "Back Pain", "Routine Checkup", "Flu"])
                billing = random.choice(["Paid", "Free"])
                
                # Phone number logic (Zambian prefixes)
                prefix = random.choice(["97", "96", "95", "77", "76"])
                digits = "".join(random.choices('0123456789', k=7))
                phone = f"+260{prefix}{digits}"

                # --- Database Check & Insertion ---
                if not patient_exists(email):
                    # Passing data to your existing save_patient function
                    success = save_patient(name, age, phone, email, address, symptoms, billing)
                    if success:
                        print(f"{index}. Added: {name} ({age} yrs) - {billing}")
                else:
                    print(f"{index}. Skipped: {name} (Already in database)")

    except FileNotFoundError:
        print("Error: patient_names_newlines.txt not found. Check the file path.")

if __name__ == "__main__":
    add_patients_batch()