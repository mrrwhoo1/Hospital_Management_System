import mysql.connector
import bcrypt
import os
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    try:
        db = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if db.is_connected():
            return db
        print("Connected")
        
    except Exception as e:
        print(f'Database Connection Error: {e}')
        return None
    
def email_exists(email):
    db = get_db_connection()
    if db:
        cursor = db.cursor()
        query  = ("select email from employees where email = %s")
        cursor.execute(query, (email,)) 
        result = cursor.fetchone()
        
        cursor.close()
        db.close()
        return result is not None
    return False

def db_connect_verifyer(username, entered_password):
    db = get_db_connection()
    if db:
        cursor = db.cursor()
            
        command = ("select role,password_hash, full_name from employees where username = %s")
        cursor.execute(command, (username,))
        result = cursor.fetchone()
        cursor.close()
        db.close()
        
        if result:
            stored_hash = result[1]
            if bcrypt.checkpw(entered_password.encode('utf-8'), stored_hash.encode('utf-8')):
                return result[0], result[2]
       
    return None
        

#--------------DASHBOARD PY----------------------------------   
def add_user(n,p_h,r,f_n,e,p):
    db = get_db_connection()
    if db:
        try:
            byte_password = p_h.encode('utf-8')
            sauce = bcrypt.gensalt()
            hashed_pass = bcrypt.hashpw(byte_password, sauce)
            
            cursor = db.cursor()
            employees_command = "insert into employees(username,password_hash,role,full_name,email,phone) VALUES (%s,%s,%s,%s,%s,%s) "
            cursor.execute(employees_command, (n,hashed_pass,r,f_n,e,p))
            db.commit()
            cursor.close()
            db.close()
            return True
        except Exception as e:
            print(f'error: {e}')
            
    return False




def get_patients_lookup():
    db = get_db_connection()
    if db:
        cursor = db.cursor()
        cursor.execute("SELECT patient_id, full_name FROM patients")
        res = cursor.fetchall()
        db.close()
        return res
    return []

def get_doctors_lookup():
    db = get_db_connection()
    if db:
        cursor = db.cursor()
        cursor.execute("SELECT user_id, full_name FROM employees WHERE role = 'Doctor'")
        res = cursor.fetchall()
        db.close()
        return res
    return []

def save_appointment(patient_id, employee_id, dept, time):
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            # Use the actual column names from your schema: patient_id, employee_id
            query = """INSERT INTO appointments (patient_id, employee_id, department, appt_time) 
                       VALUES (%s, %s, %s, %s)"""
            cursor.execute(query, (patient_id, employee_id, dept, time))
            db.commit()
            cursor.close()
            db.close()
            return True
        except Exception as e:
            print(f"Error saving appointment: {e}")
    return False

def delete_appointment(appt_id):
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            query = "DELETE FROM appointments WHERE appt_id = %s"
            cursor.execute(query, (appt_id,))
            db.commit()
            cursor.close()
            db.close()
            return True
        except Exception as e:
            print(f"Error deleting appointment: {e}")
    return False

def get_all_appointments():
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            query = """
                SELECT 
                    a.appt_id, 
                    a.appt_time, 
                    p.full_name, 
                    e.full_name, 
                    a.department, 
                    a.status,
                    a.patient_id,   
                    a.employee_id   
                FROM appointments a
                JOIN patients p ON a.patient_id = p.patient_id
                JOIN employees e ON a.employee_id = e.user_id
                ORDER BY a.appt_time ASC
            """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            db.close()
            return result
        except Exception as e:
            print(f"Error fetching appointments: {e}")
    return []

def update_appointment(appt_id, patient_id, employee_id, dept, time, status):
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            query = """UPDATE appointments 
                       SET patient_id = %s, employee_id = %s, department = %s, 
                           appt_time = %s, status = %s 
                       WHERE appt_id = %s"""
            cursor.execute(query, (patient_id, employee_id, dept, time, status, appt_id))
            db.commit()
            cursor.close()
            db.close()
            return True
        except Exception as e:
            print(f"Error updating appointment: {e}")
    return False


#-------------PATIENTS PY----------------------------------------------
def search_patients(search_query):
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            # The % symbols allow for partial matches (e.g., "Ma" finds "Maron")
            query = "SELECT patient_id, full_name, age, contact, billing_type FROM patients WHERE full_name LIKE %s"
            cursor.execute(query, (f"%{search_query}%",))
            result = cursor.fetchall()
            cursor.close()
            db.close()
            return result
        except Exception as e:
            print(f"Search Error: {e}")
    return []


def save_patient(name, age, contact, email, address, symptoms, billing):
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            query = """INSERT INTO patients (full_name, age, contact, email, address, symptoms, billing_type) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(query, (name, age, contact, email, address, symptoms, billing))
            db.commit()
            cursor.close()
            db.close()
            return True
        except Exception as e:
            print(f"Error saving patient: {e}")
    return False

def get_all_patients():
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            # We add 'LIMIT 20' to keep the UI snappy and fast
            cursor.execute("""
                SELECT patient_id, full_name, age, contact, billing_type 
                FROM patients 
                ORDER BY patient_id
            """)
            result = cursor.fetchall()
            cursor.close()
            db.close()
            return result
        except Exception as e:
            print(f"Error fetching patients: {e}")
    return []

def delete_patient(patient_id):
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("DELETE FROM patients WHERE patient_id = %s", (patient_id,))
            db.commit()
            cursor.close()
            db.close()
            return True
        except Exception as e:
            print(f"Error deleting patient: {e}")
    return False

def update_patient(patient_id, name, age, contact, email, address, symptoms, billing):
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            query = """
                UPDATE patients 
                SET full_name = %s, age = %s, contact = %s, 
                    email = %s, address = %s, symptoms = %s, billing_type = %s 
                WHERE patient_id = %s
            """
            cursor.execute(query, (name, age, contact, email, address, symptoms, billing, patient_id))
            db.commit()
            cursor.close()
            db.close()
            return True
        except Exception as e:
            print(f"Error updating patient: {e}")
    return False


#---------Auto Patient Add------------------------------------
def patient_exists(email):
    db = get_db_connection()
    if db:
        cursor = db.cursor()
        query = "SELECT email FROM patients WHERE email = %s"
        cursor.execute(query, (email,)) 
        result = cursor.fetchone()
        cursor.close()
        db.close()
        return result is not None
    return False

def get_upcoming_appointments(limit=5):
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("""
                SELECT appt_id, appt_time, patient_name, doctor_name, department, status
                FROM appointments
                WHERE appt_time >= NOW()
                ORDER BY appt_time ASC
                LIMIT %s
            """, (limit,))
            result = cursor.fetchall()
            cursor.close()
            db.close()
            return result
        except Exception as e:
            print(f"Error fetching upcoming appointments: {e}")
    return []


#-------------PAYMENTS PY----------------------------------------------
def save_payment(patient_id, amount, method, status, notes):
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("""
                INSERT INTO payments (patient_id, amount, method, status, notes)
                VALUES (%s, %s, %s, %s, %s)
            """, (patient_id, amount, method, status, notes))
            db.commit()
            cursor.close()
            db.close()
            return True
        except Exception as e:
            print(f"Error saving payment: {e}")
    return False


def get_all_payments():
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("""
                SELECT p.payment_id, pt.full_name, p.amount, p.method, p.status, p.created_at
                FROM payments p
                JOIN patients pt ON p.patient_id = pt.patient_id
                ORDER BY p.created_at DESC
            """)
            result = cursor.fetchall()
            cursor.close()
            db.close()
            return result
        except Exception as e:
            print(f"Error fetching payments: {e}")
    return []


def search_payments(search_query):
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("""
                SELECT p.payment_id, pt.full_name, p.amount, p.method, p.status, p.created_at
                FROM payments p
                JOIN patients pt ON p.patient_id = pt.patient_id
                WHERE pt.full_name LIKE %s
                ORDER BY p.created_at DESC
            """, (f"%{search_query}%",))
            result = cursor.fetchall()
            cursor.close()
            db.close()
            return result
        except Exception as e:
            print(f"Search payments error: {e}")
    return []


def delete_payment(payment_id):
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("DELETE FROM payments WHERE payment_id = %s", (payment_id,))
            db.commit()
            cursor.close()
            db.close()
            return True
        except Exception as e:
            print(f"Error deleting payment: {e}")
    return False


def get_payment_summary():
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("""
                SELECT
                    COALESCE(SUM(CASE WHEN status = 'Paid' THEN amount ELSE 0 END), 0),
                    COUNT(CASE WHEN status = 'Paid'    THEN 1 END),
                    COUNT(CASE WHEN status = 'Pending' THEN 1 END),
                    COUNT(CASE WHEN status = 'Overdue' THEN 1 END)
                FROM payments
            """)
            row = cursor.fetchone()
            cursor.close()
            db.close()
            if row:
                return {
                    "total_revenue": float(row[0]),
                    "paid_count":    row[1],
                    "pending_count": row[2],
                    "overdue_count": row[3],
                }
        except Exception as e:
            print(f"Error fetching payment summary: {e}")
    return {"total_revenue": 0, "paid_count": 0, "pending_count": 0, "overdue_count": 0}


def get_all_patients_simple():
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("SELECT patient_id, full_name FROM patients ORDER BY full_name ASC")
            result = cursor.fetchall()
            cursor.close()
            db.close()
            return result
        except Exception as e:
            print(f"Error fetching patients for dropdown: {e}")
    return []


#-------------EMPLOYEES PY----------------------------------------------
def get_all_employees():
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("""
                SELECT user_id, full_name, username, role, email, phone, created_at
                FROM employees
                ORDER BY created_at DESC
            """)
            result = cursor.fetchall()
            cursor.close()
            db.close()
            return result
        except Exception as e:
            print(f"Error fetching employees: {e}")
    return []


def search_employees(search_query):
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("""
                SELECT user_id, full_name, username, role, email, phone, created_at
                FROM employees
                WHERE full_name LIKE %s OR username LIKE %s
                ORDER BY created_at DESC
            """, (f"%{search_query}%", f"%{search_query}%"))
            result = cursor.fetchall()
            cursor.close()
            db.close()
            return result
        except Exception as e:
            print(f"Search employees error: {e}")
    return []


def delete_employee(emp_id):
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("DELETE FROM employees WHERE user_id = %s", (emp_id,))
            db.commit()
            cursor.close()
            db.close()
            return True
        except Exception as e:
            print(f"Error deleting employee: {e}")
    return False


def update_employee(emp_id, full_name, username, role, email, phone):
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            cursor.execute("""
                UPDATE employees
                SET full_name = %s, username = %s, role = %s, email = %s, phone = %s
                WHERE user_id = %s
            """, (full_name, username, role, email, phone, emp_id))
            db.commit()
            cursor.close()
            db.close()
            return True
        except Exception as e:
            print(f"Error updating employee: {e}")
    return False


#-------------DASHBOARD PY----------------------------------------------
def get_dashboard_stats():
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()

            cursor.execute("SELECT COUNT(*) FROM patients")
            total_patients = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM appointments")
            total_appointments = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM employees WHERE role = 'Doctor'")
            total_doctors = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM patients WHERE billing_type = 'Paid'")
            paid_patients = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM patients WHERE billing_type = 'Free'")
            free_patients = cursor.fetchone()[0]

            cursor.execute("""
                SELECT full_name, status FROM employees
                WHERE role = 'Doctor'
                ORDER BY full_name ASC
                LIMIT 6
            """)
            doctors_list = cursor.fetchall()

            cursor.close()
            db.close()
            return {
                "total_patients":     total_patients,
                "total_appointments": total_appointments,
                "total_doctors":      total_doctors,
                "paid_patients":      paid_patients,
                "free_patients":      free_patients,
                "doctors_list":       doctors_list,
            }
        except Exception as e:
            print(f"Error fetching dashboard stats: {e}")
    return {
        "total_patients": 0, "total_appointments": 0,
        "total_doctors": 0, "paid_patients": 0,
        "free_patients": 0, "doctors_list": [],
    }


#------------------------Change accent color--------------
def update_user_accent(username, color_code):
    db = get_db_connection()
    if db:
        try:
            cursor = db.cursor()
            query = "UPDATE employees SET accent_color = %s WHERE username = %s"
            cursor.execute(query, (color_code, username))
            db.commit()
            cursor.close()
            db.close()
            return True
        except Exception as e:
            print(f"Error updating accent: {e}")
    return False