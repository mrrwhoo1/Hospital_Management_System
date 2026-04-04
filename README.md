**Hospital Management System (HMS) — Beta v0.1.0**

A professional-grade, dark-themed desktop application built for streamlined healthcare administration. Developed as part of the IT212 Assignment, this system leverages Python 3.12, CustomTkinter, and MySQL to provide a robust CRUD interface for hospital operations.

Note: This project is currently in Active Beta. It is functional but undergoing performance optimizations for large-scale data handling to prevent UI hanging.

**Image Previews;**

<img width="600" height="400" alt="Screenshot from 2026-04-04 16-17-12" src="https://github.com/user-attachments/assets/b7c40d33-c4ec-4ac4-a1c0-79d95212054b" />
<img width="600" height="400" alt="Screenshot from 2026-04-04 16-17-21" src="https://github.com/user-attachments/assets/31917e7c-7dbd-43bd-96b4-563ac11d16bc" />
<img width="600" height="400" alt="Screenshot from 2026-04-04 16-17-30" src="https://github.com/user-attachments/assets/f12e6e9b-e32d-4204-9de4-e15b8d9a9990" />
<img width="600" height="400" alt="Screenshot from 2026-04-04 16-17-49" src="https://github.com/user-attachments/assets/a3bbfef2-abc7-4679-917b-86def108f5d0" />
<img width="600" height="400" alt="Screenshot from 2026-04-04 16-17-59" src="https://github.com/user-attachments/assets/460ef488-6a8f-4be9-a3ad-5f2bea88f328" />

**Core Features**

**Secure Authentication**
Role-Based Access: STILL BEING IMPLEMENTED!

Security: Industry-standard password hashing using Bcrypt for user credentials.

Environment Safety: Sensitive database credentials managed via .env files using python-dotenv to prevent hardcoding secrets.

**Patient & Employee Management**
Full CRUD: Create, Read, Update, and Delete records with real-time MySQL synchronization.

Modern UI: Built with CustomTkinter for a native Ubuntu "Dark Mode" aesthetic on Lenovo ThinkPad hardware.

Automated Seeding: Custom Python scripts to batch-import patient and employee data from formatted .txt files—perfect for rapid testing and deployment.

**Database Architecture**

Relational Mapping: Clean SQL schema handling relationships between Patients, Appointments, and Staff.

Modular Logic: Database operations are isolated in db_connector.py for easier debugging and maintenance.

**Technical Stack**

1. Component	Technology
2. Language	Python 3.12 (Running on Ubuntu Linux)
3.Frontend	CustomTkinter (Modernized Tkinter UI)
4. Backend	MySQL (Relational Database)
5. Security	Bcrypt (Hashing), Dotenv (Secrets Management)
6. Packaging	PyInstaller (Standalone Linux Binary)


**Installation & Setup (Ubuntu/Linux)**
1. Clone the Repository
Bash
git clone https://github.com/mrrwhoo1/Hospital_Management_System.git
cd Hospital_Management_System
2. Configure the Environment
Create a .env file in the root directory:

DB_HOST=localhost
DB_USER=your_username
DB_PASS=your_password
DB_NAME=hp_management_sys

3. Initialize the Database
Import the schema into your MySQL instance:

Bash
mysql -u your_username -p < schema.sql
4. Install Dependencies
Ensure you are in your virtual environment, then run:

Bash
pip install customtkinter mysql-connector-python bcrypt python-dotenv pillow

5. Launch the Application
Bash
python IT212_Assignment_by_121682.py
**Performance & Beta Limitations**

Single-Threaded UI: Currently, database queries run on the main thread. Loading 100+ records may cause a temporary UI hang (the "Loading Freeze").

Linux Binary: The standalone .bin file in the releases requires a local .env and an active MySQL server to function.

Module Completion: Payment and Invoicing logic is currently in the "UI Placeholder" stage and will be finalized in future updates.

**Development Roadmap**
[ ] Explore ways to get rid of freezing when you first open it.

[ ] Reporting: Add functionality to export patient lists to PDF or CSV formats.

[ ] Cross-Platform Support: Test and compile a .exe version for Windows users. 

**Academic Context**
**Created by Maron H. Chilomo Computer Science Student @ Cavendish University, Zambia.**
