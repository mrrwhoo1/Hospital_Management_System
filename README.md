# Smart Health — Hospital Management System
### Beta v0.2.0

A professional-grade desktop application built for streamlined healthcare administration. Developed as part of the IT212 Assignment at Cavendish University, Zambia. This release is a significant architectural upgrade over v0.1 — the UI framework has been fully migrated from CustomTkinter to **Python Flet**, the entire codebase has been refactored into an **object-oriented class-based architecture**, and several new modules have been added.

> **Note:** This project is in Active Beta. Core features are functional. Payment write operations and persistent chat remain UI placeholders scheduled for v0.3.

---

## What's New in v0.2.0

| Area | v0.1.0 | v0.2.0 |
|---|---|---|
| UI Framework | CustomTkinter (Tkinter-based) | **Python Flet** (Flutter-based) |
| Code Architecture | **Object-Oriented (classes)** | **Object-Oriented (classes)** |
| Navigation | Single-window views | **Sidebar shell with dynamic view switching** |
| Patient Module | Basic CRUD | CRUD + live search + DB auto-ID |
| New Modules | — | Appointments, Payments, Employee, Help, Settings, Bug Tracker |
| Backwards Compatibility | — | Shim functions preserve old call signatures |
| Bug Fix | Lambda closure bug in delete | **Fixed — uses default-argument capture** |
| UI Freeze | Present on data load | **Reduced — ListView replaces blocking renders** |

---

## Image Previews

Login Page Comparison

<p align="center">
<img src="https://github.com/user-attachments/assets/eb5b111f-a30d-44b4-aa13-94fdb2d5e092" width="400" alt="Former Login">
<img src="https://github.com/user-attachments/assets/e12abb5b-9b9f-40f0-98d3-243515d2eed7" width="400" alt="Current Login">
</p>

Dashboard Comparison (Performance Boost)

<p align="center">
<img src="https://github.com/user-attachments/assets/943c0bda-d526-40d6-aeb1-080d21c8a633" width="400" alt="Former Dashboard">
<img src="https://github.com/user-attachments/assets/9e440439-2ad6-422a-a67c-71bd169f2e2a" width="400" alt="Current Dashboard">
</p>
Note: The former version failed to render data after 2 minutes; the Flet version loads instantly.

Patients Page

<p align="center">
<img src="https://github.com/user-attachments/assets/230b1f6c-8191-43bb-95aa-494aacdff4ac" width="400" alt="Former Patients">
<img src="https://github.com/user-attachments/assets/e902904d-ac96-4075-b751-4a6658c1ee46" width="400" alt="Current Patients">
</p>

Appointments

<p align="center">
<img src="https://github.com/user-attachments/assets/d65ea39b-c2bf-45b6-8b09-91f40326362e" width="400" alt="Former Appointments">
<img src="https://github.com/user-attachments/assets/d52bfb6e-a5d1-4c47-a0db-60e160f77567" width="400" alt="Current Appointments">
</p>

Payments & Financials

<p align="center">
<img src="https://github.com/user-attachments/assets/2dc24ee4-292a-45fc-bc04-5a5d4a7dd62d" width="400" alt="Former Payments">
<img src="https://github.com/user-attachments/assets/38dbeda4-f1dc-4344-b2ea-c24fb13474fd" width="400" alt="Current Payments">
</p>

Staff / Employee Directory

<p align="center">
<img src="https://github.com/user-attachments/assets/8aa119c1-90da-49f2-b616-bb9255f3565d" width="400" alt="Former Employees">
<img src="https://github.com/user-attachments/assets/db9beb5e-01e4-4cbe-ac6b-7d1b0b2eb18e" width="400" alt="Current Employees">
</p>

Help & Support Center

<p align="center">
<img src="https://github.com/user-attachments/assets/dfeb95da-6e7e-4ec7-bc99-d300a62bb1e0" width="400" alt="Former Help">
<img src="https://github.com/user-attachments/assets/e451c09b-64ed-4201-9c0c-9acb4487183c" width="400" alt="Current Help">
</p>

Settings

<p align="center">
<img src="https://github.com/user-attachments/assets/52b722ec-9bea-4615-9b7d-ee32225be0f6" width="400" alt="Former Settings">
<img src="https://github.com/user-attachments/assets/0d4435ce-a1aa-479b-be62-870075e9d55f" width="400" alt="Current Settings">
</p>

New Feature: Analytics & Reports

<p align="center">
<img src="https://github.com/user-attachments/assets/eafe0f44-0a16-4066-ab9f-f28ad94b6e03" width="820" alt="New Report Module">
</p>



---

## Core Features

### Secure Authentication
- **Role-based login:** Credentials verified against the database via `db_connector.py`. User name and role are retrieved on login and passed to all modules.
- **Password security:** Industry-standard hashing via Bcrypt.
- **Environment safety:** Database credentials managed through `.env` files using `python-dotenv` — no hardcoded secrets.
- **Role enforcement:** UI-level role restrictions are planned for v0.3; role is captured and threaded through all modules in preparation.

### Dashboard
- Live stat cards fetched from the database on every login: total patients, appointments, doctors on duty, and paid patients.
- Built-in doctor consultation chat panel (session-only; persistent messaging planned for v0.3).
- Sidebar navigation shell giving one-click access to all modules.

### Patient Management
- Full CRUD: register, search by name, and delete patient records with real-time MySQL synchronisation.
- Registration modal captures: full name, age, billing type, contact, email, home address, and symptoms.
- Database auto-assigns patient IDs — no manual ID entry required.
- Success confirmation via snack bar; list auto-refreshes after every write.

### Appointments
- Daily timeline view with colour-coded status indicators: Confirmed (green), Pending (amber), Cancelled (red).
- Header summary showing total, pending, and urgent appointment counts for the day.

### Payments
- Financial summary header showing total revenue and pending balance.
- Scrollable transaction ledger with reference numbers, patient names, services, amounts, and paid/unpaid status.
- Print receipt button present per row (invoice generation planned for v0.3).

### Employee Management
- Scrollable staff directory with role-colour-coded avatars: Doctor, Nurse, Admin, Pharmacist.
- Per-staff popup menu with View Profile and Assign Shift actions.
- Staff search field and Add Staff button (write functionality planned for v0.3).

### Help, Settings & Bug Tracker
- **Help Centre:** Searchable topic grid covering Getting Started, Patient Records, Billing, Scheduling, Staff, and Security. 24/7 support contact button.
- **Settings:** Account security (password, 2FA), system preferences (dark mode toggle, language, auto-save), and notification preferences.
- **Bug Tracker:** Submit tickets with title and detail description. Scrollable ticket history with Open / In Progress / Resolved status badges.

---

## Technical Stack

| Component | Technology |
|---|---|
| Language | Python 3.12 (Fedora Linux) |
| UI Framework | **Flet** (Flutter-based cross-platform desktop) |
| Database | MySQL (Relational) |
| DB Abstraction | `db_connector.py` (custom module) |
| Security | Bcrypt (password hashing), python-dotenv (secrets) |
| Architecture | OOP — one class per module, `build()` pattern |
| Packaging | PyInstaller (standalone Linux binary) |

---

## Project Structure

```
src/
├── main.py              # Entry point — SmartHealthApp class
├── homepage.py          # HomeUI class — sidebar shell + dashboard
├── patientspage.py      # PatientUI class — full CRUD
├── appointments.py      # AppointmentsUI class — timeline view
├── paymentspage.py      # PaymentsUI class — financial ledger
├── employee.py          # EmployeeUI class — staff directory
├── helppage.py          # HelpUI class — help centre
├── settingspage.py      # SettingsUI class — preferences
├── reportpage.py        # BugReportUI class — issue tracker
├── db_connector.py      # Database abstraction layer
└── assets/
    └── background.png
.env                     # DB credentials (not committed to repo)
schema.sql               # MySQL schema
requirements.txt
```

---

## Installation & Setup (Ubuntu / Linux)

**1. Clone the repository**
```bash
git clone https://github.com/mrrwhoo1/Hospital_Management_System.git
cd Hospital_Management_System
```

**2. Create and activate a virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**3. Configure the environment**

Create a `.env` file in the root directory:
```
DB_HOST=localhost
DB_USER=your_username
DB_PASS=your_password
DB_NAME=hp_management_sys
```

**4. Initialize the database**
```bash
mysql -u your_username -p < schema.sql
```

**5. Install dependencies**
```bash
pip install -r requirements.txt
```

**6. Launch the application**
```bash
python src/main.py
```

---

## Known Limitations (Beta v0.2)

- **Consultation chat is session-only.** Messages are not persisted to the database. Persistent multi-user messaging requires a backend broker and is scheduled for v0.3.
- **Role-based UI restrictions not yet enforced.** All authenticated users can access all modules regardless of role. Role is captured at login and threaded through all classes in preparation for v0.3 enforcement.
- **Dark mode toggle is wired but inactive.** The Settings switch exists; theme switching will be implemented in v0.3.
- **Linux only** for the standalone binary. The `.bin` release requires a local `.env` and an active MySQL server.
- **Help page, setting and report** are just static as at now and offer no real value.

---

## Development Roadmap

- [x] Migrate UI framework from CustomTkinter to Flet
- [x] Refactor all modules from functions to OOP classes
- [x] Add Appointments, Payments, Employee, Help, Settings, and Bug Tracker modules
- [x] Fix lambda closure bug in patient delete
- [x] Reduce UI freeze via Flet ListView (replaces blocking renders)
- [ ] Enforce role-based access control at the UI level
- [x] Wire appointment and payment write operations to the database
- [x] Complete staff registration modal
- [ ] Implement persistent doctor consultation chat
- [ ] Activate dark mode theme switching
- [ ] Export patient records to PDF or CSV
- [ ] Cross-platform: compile and test a Windows `.exe` build
- [ ] Migrate single-threaded DB queries to async/background threads to eliminate remaining UI freeze on large datasets
- [ ] connect reports page to the database
- [ ] implement profile picture handling
- [ ] add real guids to the help & center page

---

## Academic Context

**Created by Maron H. Chilomo**  
Computer Science Student @ Cavendish University, Zambia  
IT212 Assignment — Beta v0.2.0
