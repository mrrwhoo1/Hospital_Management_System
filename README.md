# Smart Health — Hospital Management System
### Beta v0.2.0

A professional-grade desktop application built for streamlined healthcare administration. Developed as part of the IT212 Assignment at Cavendish University, Zambia. This release is a significant architectural upgrade over v0.1 — the UI framework has been fully migrated from CustomTkinter to **Python Flet**, the entire codebase has been refactored into an **object-oriented class-based architecture**, and several new modules have been added.

> **Note:** This project is in Active Beta. Core features are functional. Payment write operations and persistent chat remain UI placeholders scheduled for v0.3.

---

## What's New in v0.2.0

| Area | v0.1.0 | v0.2.0 |
|---|---|---|
| UI Framework | CustomTkinter (Tkinter-based) | **Python Flet** (Flutter-based) |
| Code Architecture | Functional (plain functions) | **Object-Oriented (classes)** |
| Navigation | Single-window views | **Sidebar shell with dynamic view switching** |
| Patient Module | Basic CRUD | CRUD + live search + DB auto-ID |
| New Modules | — | Appointments, Payments, Employee, Help, Settings, Bug Tracker |
| Backwards Compatibility | — | Shim functions preserve old call signatures |
| Bug Fix | Lambda closure bug in delete | **Fixed — uses default-argument capture** |
| UI Freeze | Present on data load | **Reduced — ListView replaces blocking renders** |

---

## Image Previews

<img width="600" height="400" alt="Dashboard view" src="https://github.com/user-attachments/assets/b7c40d33-c4ec-4ac4-a1c0-79d95212054b" />
<img width="600" height="400" alt="Patient registry" src="https://github.com/user-attachments/assets/31917e7c-7dbd-43bd-96b4-563ac11d16bc" />
<img width="600" height="400" alt="Appointments timeline" src="https://github.com/user-attachments/assets/f12e6e9b-e32d-4204-9de4-e15b8d9a9990" />
<img width="600" height="400" alt="Payments ledger" src="https://github.com/user-attachments/assets/a3bbfef2-abc7-4679-917b-86def108f5d0" />
<img width="600" height="400" alt="Staff directory" src="https://github.com/user-attachments/assets/460ef488-6a8f-4be9-a3ad-5f2bea88f328" />

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
| Language | Python 3.12 (Ubuntu Linux) |
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
- **Appointment and payment data is partially static.** The timeline and ledger display correctly but write operations (creating/updating appointments and payments) are not yet wired to the database.
- **Staff registration modal is a placeholder.** The Add Staff button and form exist in the UI but do not write to the database yet.
- **Role-based UI restrictions not yet enforced.** All authenticated users can access all modules regardless of role. Role is captured at login and threaded through all classes in preparation for v0.3 enforcement.
- **Dark mode toggle is wired but inactive.** The Settings switch exists; theme switching will be implemented in v0.3.
- **Linux only** for the standalone binary. The `.bin` release requires a local `.env` and an active MySQL server.

---

## Development Roadmap

- [x] Migrate UI framework from CustomTkinter to Flet
- [x] Refactor all modules from functions to OOP classes
- [x] Add Appointments, Payments, Employee, Help, Settings, and Bug Tracker modules
- [x] Fix lambda closure bug in patient delete
- [x] Reduce UI freeze via Flet ListView (replaces blocking renders)
- [ ] Enforce role-based access control at the UI level
- [ ] Wire appointment and payment write operations to the database
- [ ] Complete staff registration modal
- [ ] Implement persistent doctor consultation chat
- [ ] Activate dark mode theme switching
- [ ] Export patient records to PDF or CSV
- [ ] Cross-platform: compile and test a Windows `.exe` build
- [ ] Migrate single-threaded DB queries to async/background threads to eliminate remaining UI freeze on large datasets

---

## Academic Context

**Created by Maron H. Chilomo**  
Computer Science Student @ Cavendish University, Zambia  
IT212 Assignment — Beta v0.2.0
