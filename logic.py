import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

PRIORITY_ORDER = {
    "Urgent": 3,
    "High": 2,
    "Standard": 1
}

SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

def get_spreadsheet():
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json", SCOPE
    )
    client = gspread.authorize(creds)
    return client.open("Skylark_Drones_Database")

def read_sheet(sheet_name):
    sheet = get_spreadsheet().worksheet(sheet_name)
    return sheet.get_all_records(), sheet
#piolet matching
def is_pilot_available(pilot, mission):
    if pilot["status"] != "Available":
        return False

    # Skill check
    pilot_skills = pilot["skills"].split(",")
    if mission["required_skills"] not in pilot_skills:
        return False

    # Certification check
    pilot_certs = pilot["certifications"].split(",")
    required_certs = mission["required_certs"].split(",")
    for cert in required_certs:
        if cert not in pilot_certs:
            return False

    # Location check
    if pilot["location"] != mission["location"]:
        return False

    return True
#drone matching
def is_drone_available(drone, mission):
    if drone["status"] != "Available":
        return False

    drone_caps = drone["capabilities"].split(",")
    if mission["required_skills"] not in drone_caps:
        return False

    if drone["location"] != mission["location"]:
        return False

    return True
#assignment function
from conflict import check_pilot_conflicts, check_drone_conflicts

def assign_mission(project_id):
    missions, mission_ws = read_sheet("missions")
    pilots, pilot_ws = read_sheet("pilot_roster")
    drones, drone_ws = read_sheet("drone_fleet")

    mission = next(m for m in missions if m["project_id"] == project_id)

    failure_reasons = []

    # 1️⃣ TRY NORMAL ASSIGNMENT
    for pilot in pilots:
        pilot_issues = check_pilot_conflicts(pilot, mission)
        if pilot_issues:
            failure_reasons.extend(pilot_issues)
            continue

        for drone in drones:
            drone_issues = check_drone_conflicts(drone, mission)
            if drone_issues:
                failure_reasons.extend(drone_issues)
                continue

            # ✅ NORMAL ASSIGNMENT
            pilot_row = pilots.index(pilot) + 2
            drone_row = drones.index(drone) + 2

            pilot_ws.update_cell(pilot_row, 6, "Assigned")
            pilot_ws.update_cell(pilot_row, 7, project_id)

            drone_ws.update_cell(drone_row, 4, "Assigned")
            drone_ws.update_cell(drone_row, 6, project_id)

            return f"✅ Assigned pilot {pilot['name']} and drone {drone['drone_id']}"

    # 2️⃣ NORMAL FAILED → PREPARE EXPLANATION
    unique_reasons = list(set(failure_reasons))
    explanation = "\n".join(unique_reasons[:5])

    # 3️⃣ 🔴 URGENT REASSIGNMENT (NO RETURN ABOVE THIS)
    if mission["priority"].strip().lower() == "urgent":
        for pilot in pilots:
            if pilot["status"] == "Assigned":
                pilot_row = pilots.index(pilot) + 2

                pilot_ws.update_cell(pilot_row, 7, project_id)

                return (
                    f"⚠️ Urgent mission detected.\n"
                    f"Reassigned pilot {pilot['name']} "
                    f"from a lower-priority mission to {project_id}"
                )

    # 4️⃣ FINAL FALLBACK
    return f"❌ No assignment possible due to:\n{explanation}"


#reassignment pilot
def find_reassignable_pilot(pilots, mission_priority):
    for pilot in pilots:
        if pilot["status"] == "Assigned":
            # Assume assigned pilots are on Standard missions
            if PRIORITY_ORDER[mission_priority] > PRIORITY_ORDER["Standard"]:
                return pilot
    return None

