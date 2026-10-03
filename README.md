# Digital E-Waste Locator

A college PBL prototype based on the project proposal:

**Digital Locator Tool for Certified E-Waste Recycling Facilities**

The prototype uses:

- HTML
- CSS
- JavaScript
- Python
- Flask
- MySQL
- Leaflet
- OpenStreetMap
- VS Code
- Git/GitHub

## What the prototype does

1. Displays verified facility records on an interactive map.
2. Allows searching by facility/city/address/category.
3. Filters by e-waste category.
4. Uses browser geolocation to find facilities within a selected radius.
5. Displays facility details:
   - address
   - contact
   - operating hours
   - accepted e-waste
   - verification source
   - last verified date
6. Provides directions through OpenStreetMap.
7. Keeps verification status in the database.

## Important data warning

The included `seed_demo.sql` contains only development/demo records.
They are deliberately marked `Pending`, so the application does not falsely
claim that invented facilities are certified.

Before your final demonstration, replace the demo records with facility data
that your team has verified from an authoritative source. Set
`verification_status` to `Verified` only after that verification.

## Setup in VS Code

### 1. Install prerequisites

Install:

- Python 3
- MySQL Server
- VS Code

Open the project folder in VS Code.

### 2. Create a Python virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```cmd
venv\Scripts\activate
```

### 3. Install packages

```bash
pip install -r requirements.txt
```

### 4. Create the database

Open MySQL Workbench or the MySQL command line and run:

```sql
SOURCE path/to/schema.sql;
```

Then optionally load the demo data:

```sql
SOURCE path/to/seed_demo.sql;
```

Again: demo records are Pending and therefore do not appear in the public
verified-facility list.

### 5. Configure database credentials

Copy:

```text
.env.example
```

to:

```text
.env
```

Then edit the values:

```text
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD
DB_NAME=ewaste_locator
```

### 6. Run the application

```bash
python app.py
```

Open the local URL shown by Flask, normally:

```text
http://127.0.0.1:5000
```

## How to add a real verified facility

Use MySQL:

```sql
USE ewaste_locator;

INSERT INTO facilities
(name, address, city, state, pincode, latitude, longitude,
 contact, email, operating_hours, accepted_categories,
 verification_status, verification_source, last_verified, website, notes)
VALUES
(
 'REAL FACILITY NAME',
 'REAL ADDRESS',
 'Mumbai',
 'Maharashtra',
 'PINCODE',
 19.0000000,
 72.0000000,
 'PHONE',
 'EMAIL',
 'Mon-Sat, 10:00 AM-6:00 PM',
 'Mobile Phones,Laptops,Computers,Batteries',
 'Verified',
 'AUTHORITATIVE SOURCE USED FOR VERIFICATION',
 '2026-09-25',
 'https://example.com',
 'Verification notes'
);
```

Only use `Verified` when your team has actually checked the record.

## Project structure

```text
e_waste_locator_project/
│
├── app.py
├── requirements.txt
├── .env.example
├── schema.sql
├── seed_demo.sql
├── README.md
│
├── templates/
│   └── index.html
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

## Mapping

The frontend uses Leaflet with OpenStreetMap tiles. The initial map is
centered on Mumbai only as a neutral starting view. The browser's
"Use My Location" button asks for the user's actual location.

## Suggested PBL demo flow

1. Start MySQL.
2. Start Flask.
3. Open the website.
4. Show the map.
5. Explain the database-driven facility records.
6. Use "Use My Location" and allow browser location permission.
7. Select an e-waste category.
8. Change the radius.
9. Click a facility.
10. Show its verification details and accepted e-waste categories.
11. Click "Get Directions".

## Future improvements

The proposal/PSD identifies regular data updating as important. Possible
future work includes:

- Admin dashboard for adding/updating facilities.
- Automated data validation.
- Better authoritative verification workflow.
- Pagination for large datasets.
- User feedback/reporting for outdated facility information.
- Deployment to a public server.
- Mobile-responsive enhancements.
