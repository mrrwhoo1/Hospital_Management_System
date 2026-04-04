**Hospital Management System (HMS)**

A modern desktop application built with Python and CustomTkinter for managing hospital operations. This project features a secure login system, patient record management, and automated data seeding.

🚀 Features
Role-Based Access: Secure authentication for Admins, Doctors, and staff using bcrypt.

Patient Records: Full CRUD (Create, Read, Update, Delete) for patient information.

Batch Import: Custom scripts to populate the database from .txt files (patient_names_newlines.txt).

Modern UI: Dark-themed interface designed for Ubuntu users.

🛠️ Tech Stack
Language: Python 3.12

GUI: CustomTkinter

Database: MySQL (Relational)

Security: Bcrypt & Python-Dotenv

📋 Prerequisites
Ensure you have MySQL Server installed and a .env file in the root directory:

Plaintext
DB_HOST=localhost
DB_USER=your_user
DB_PASS=your_password
DB_NAME=hp_management_sys
⚙️ Installation
Clone the Repo:

Bash
git clone https://github.com/mrrwhoo1/hospital_management_system.git
Setup Database:
Import the schema into your MySQL instance:

Bash
mysql -u root -p < schema.sql
Install Requirements:

Bash
pip install customtkinter mysql-connector-python bcrypt python-dotenv
Run:

Bash
python IT212_Assignment_by_121682.py
⚠️ Known Issues & Limitations
Performance: As CustomTkinter runs on a single thread, loading large datasets (100+ records) may cause temporary UI "freezing" while the database query executes. Will work on making it faster on the next few updates.

In Progress: Some advanced reporting modules are currently under development.

🗺️ Roadmap
[ ] Implement Threading for database queries to keep the UI responsive.

[ ] Add pagination for the patient list view.

[ ] Complete the billing and invoicing module.
