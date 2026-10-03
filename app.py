import math
import os
import sqlite3
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request

load_dotenv()

app = Flask(__name__)

DB_FILE = os.path.join(os.path.dirname(__file__), "ewaste_locator.db")

def get_db():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()
    
    # Create table if not exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS facilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT,
            city TEXT,
            state TEXT,
            pincode TEXT,
            latitude REAL,
            longitude REAL,
            contact TEXT,
            email TEXT,
            operating_hours TEXT,
            accepted_categories TEXT,
            verification_status TEXT,
            verification_source TEXT,
            last_verified TEXT,
            website TEXT,
            notes TEXT
        )
    """)
    
    # Check if empty
    cur.execute("SELECT COUNT(*) as cnt FROM facilities")
    row = cur.fetchone()
    if row["cnt"] == 0:
        print("Seeding database with demo data...")
        demo_facilities = [
            (
                "GreenTech Recyclers Delhi", "Okhla Industrial Area Phase 1", "New Delhi", "Delhi", "110020",
                28.5273, 77.2789, "9876543210", "contact@greentechdelhi.in", "Mon-Sat 9AM-6PM",
                "Mobile Phones, Laptops, Batteries, Printers", "Verified", "State Pollution Board",
                "2023-10-01T10:00:00", "www.greentechdelhi.in", "Authorized recycler"
            ),
            (
                "EcoWaste Solutions NCR", "Udyog Vihar Phase 4", "Gurugram", "Haryana", "122015",
                28.4986, 77.0862, "9876543211", "info@ecowastencr.in", "Mon-Fri 10AM-5PM",
                "Monitors, Keyboards, Appliances", "Verified", "Central Pollution Board",
                "2023-09-15T11:30:00", "www.ecowastencr.in", "Free pickup for bulk items"
            ),
            (
                "Silicon Recovery BLR", "Electronic City Phase 1", "Bangalore", "Karnataka", "560100",
                12.8452, 77.6602, "9876543212", "hello@siliconrecovery.in", "Mon-Sat 9AM-5PM",
                "Mobile Phones, Laptops, Motherboards", "Verified", "State Pollution Board",
                "2023-08-20T14:00:00", "www.siliconrecovery.in", "Data destruction certificate provided"
            ),
            (
                "Koramangala E-Safe", "Koramangala 4th Block", "Bangalore", "Karnataka", "560034",
                12.9345, 77.6266, "9876543213", "esafe@koramangala.in", "Mon-Sun 10AM-8PM",
                "Cables, Small Appliances, Batteries", "Verified", "Local Municipality",
                "2023-10-05T09:15:00", "", "Drop-off bin only"
            ),
            (
                "Chennai E-Waste Mgmt", "Guindy Industrial Estate", "Chennai", "Tamil Nadu", "600032",
                13.0102, 80.2156, "9876543214", "support@chennaie-waste.com", "Mon-Sat 8AM-4PM",
                "Laptops, Desktop Computers, Printers", "Verified", "State Pollution Board",
                "2023-07-10T16:45:00", "www.chennaie-waste.com", "Authorized e-waste dismantler"
            ),
            (
                "Hyderabad Tech Recycle", "HITEC City", "Hyderabad", "Telangana", "500081",
                17.4435, 78.3772, "9876543215", "recycle@hydtech.in", "Mon-Fri 9AM-6PM",
                "Servers, Networking Gear, Mobile Phones", "Verified", "State Pollution Board",
                "2023-09-22T10:30:00", "www.hydtech.in", "Specializes in enterprise e-waste"
            ),
            (
                "Pune Green Electronics", "Hinjewadi IT Park", "Pune", "Maharashtra", "411057",
                18.5913, 73.7389, "9876543216", "contact@punegreen.com", "Mon-Sat 10AM-6PM",
                "Laptops, Batteries, Chargers, Monitors", "Verified", "Central Pollution Board",
                "2023-08-05T13:20:00", "www.punegreen.com", "Walk-in drop off available"
            ),
            (
                "Kolkata E-Scrap Hub", "Salt Lake Sector V", "Kolkata", "West Bengal", "700091",
                22.5735, 88.4331, "9876543217", "info@kolkataescrap.in", "Mon-Fri 10AM-5PM",
                "Motherboards, CPUs, Televisions", "Verified", "State Pollution Board",
                "2023-10-02T11:00:00", "www.kolkataescrap.in", "CRT monitor disposal accepted"
            )
        ]
        
        cur.executemany("""
            INSERT INTO facilities (
                name, address, city, state, pincode, latitude, longitude,
                contact, email, operating_hours, accepted_categories,
                verification_status, verification_source, last_verified, website, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, demo_facilities)
        conn.commit()
    
    cur.close()
    conn.close()

# Initialize DB when the module is loaded
try:
    init_db()
    print("Database initialized successfully.")
except Exception as e:
    print(f"Warning: DB init error: {e}")


def haversine_km(lat1, lon1, lat2, lon2):
    """Return distance between two latitude/longitude points in km."""
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


def row_to_dict(row):
    categories = [x.strip() for x in (row["accepted_categories"] or "").split(",") if x.strip()]
    return {
        "id": row["id"],
        "name": row["name"],
        "address": row["address"],
        "city": row["city"],
        "state": row["state"],
        "pincode": row["pincode"],
        "latitude": float(row["latitude"]),
        "longitude": float(row["longitude"]),
        "contact": row["contact"],
        "email": row["email"],
        "operating_hours": row["operating_hours"],
        "accepted_categories": categories,
        "verification_status": row["verification_status"],
        "verification_source": row["verification_source"],
        "last_verified": row["last_verified"] if row["last_verified"] else None,
        "website": row["website"],
        "notes": row["notes"],
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.get("/api/categories")
def categories():
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT DISTINCT accepted_categories
            FROM facilities
            WHERE verification_status = 'Verified'
            ORDER BY accepted_categories
        """)
        values = set()
        for row in cur.fetchall():
            for item in (row["accepted_categories"] or "").split(","):
                item = item.strip()
                if item:
                    values.add(item)
        return jsonify(sorted(values))
    finally:
        cur.close()
        conn.close()


@app.get("/api/facilities")
def facilities():
    lat = request.args.get("lat", type=float)
    lng = request.args.get("lng", type=float)
    category = request.args.get("category", "").strip()
    query = request.args.get("q", "").strip().lower()
    radius = request.args.get("radius", default=50, type=float)

    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, name, address, city, state, pincode,
                   latitude, longitude, contact, email, operating_hours,
                   accepted_categories, verification_status,
                   verification_source, last_verified, website, notes
            FROM facilities
            WHERE verification_status = 'Verified'
            ORDER BY name
        """)
        rows = cur.fetchall()
    finally:
        cur.close()
        conn.close()

    results = []
    for row in rows:
        haystack = " ".join([
            row["name"] or "", row["address"] or "", row["city"] or "",
            row["state"] or "", row["accepted_categories"] or ""
        ]).lower()

        if query and query not in haystack:
            continue

        cats = [x.strip().lower() for x in (row["accepted_categories"] or "").split(",")]
        if category and category.lower() not in cats:
            continue

        item = row_to_dict(row)

        if lat is not None and lng is not None:
            item["distance_km"] = round(
                haversine_km(lat, lng, item["latitude"], item["longitude"]), 2
            )
            if item["distance_km"] > radius:
                continue
        else:
            item["distance_km"] = None

        results.append(item)

    results.sort(key=lambda x: (
        x["distance_km"] is None,
        x["distance_km"] if x["distance_km"] is not None else 0,
        x["name"].lower()
    ))
    return jsonify(results)


@app.get("/api/facilities/<int:facility_id>")
def facility_detail(facility_id):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT id, name, address, city, state, pincode,
                   latitude, longitude, contact, email, operating_hours,
                   accepted_categories, verification_status,
                   verification_source, last_verified, website, notes
            FROM facilities
            WHERE id = ? AND verification_status = 'Verified'
        """, (facility_id,))
        row = cur.fetchone()
        if not row:
            return jsonify({"error": "Facility not found"}), 404
        return jsonify(row_to_dict(row))
    finally:
        cur.close()
        conn.close()


@app.get("/health")
def health():
    try:
        conn = get_db()
        conn.close()
        return jsonify({"status": "ok", "database": "connected", "time": datetime.now().isoformat()})
    except Exception as exc:
        return jsonify({"status": "error", "database": str(exc)}), 500


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
