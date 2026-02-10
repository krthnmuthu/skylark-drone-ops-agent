def check_pilot_conflicts(pilot, mission):
    reasons = []

    if pilot["status"] != "Available":
        reasons.append(f"Pilot {pilot['name']} is {pilot['status']}")

    pilot_skills = pilot["skills"].split(",")
    if mission["required_skills"] not in pilot_skills:
        reasons.append(
            f"Pilot {pilot['name']} lacks skill {mission['required_skills']}"
        )

    pilot_certs = pilot["certifications"].split(",")
    required_certs = mission["required_certs"].split(",")
    for cert in required_certs:
        if cert not in pilot_certs:
            reasons.append(
                f"Pilot {pilot['name']} lacks certification {cert}"
            )

    if pilot["location"] != mission["location"]:
        reasons.append(
            f"Pilot {pilot['name']} is in {pilot['location']}, mission in {mission['location']}"
        )

    return reasons
#drone check conflicts
def check_drone_conflicts(drone, mission):
    reasons = []

    if drone["status"] != "Available":
        reasons.append(
            f"Drone {drone['drone_id']} is {drone['status']}"
        )

    drone_caps = drone["capabilities"].split(",")
    if mission["required_skills"] not in drone_caps:
        reasons.append(
            f"Drone {drone['drone_id']} lacks capability {mission['required_skills']}"
        )

    if drone["location"] != mission["location"]:
        reasons.append(
            f"Drone {drone['drone_id']} is in {drone['location']}, mission in {mission['location']}"
        )

    return reasons
