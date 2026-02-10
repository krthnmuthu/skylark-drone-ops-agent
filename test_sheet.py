import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Scope for Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)

client = gspread.authorize(creds)

# Open your Google Sheet (EXACT name)
spreadsheet = client.open("Skylark_Drones_Database")

# Access pilot_roster sheet
pilot_ws = spreadsheet.worksheet("pilot_roster")
# Access drone_fleet
drone_ws = spreadsheet.worksheet("drone_fleet")
drones = drone_ws.get_all_records()
print("\nDrones data:")
for d in drones:
    print(d)

# Access missions
mission_ws = spreadsheet.worksheet("missions")
missions = mission_ws.get_all_records()
print("\nMissions data:")
for m in missions:
    print(m)


# READ data
pilots = pilot_ws.get_all_records()
print("Pilots data:")
for p in pilots:
    print(p)

# WRITE test (update first pilot status)
pilot_ws.update_cell(2, 6, "Available")

print("✅ Sheet read & write successful")
