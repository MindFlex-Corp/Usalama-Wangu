import csv

from models.incidents import Incident


def is_duplicate_incident(incident_name: str, seen_names: set) -> bool:
    return incident_name in seen_names


def is_complete_incident(incident: dict, required_keys: list) -> bool:
    return all(key in incident for key in required_keys)


def save_incidents_to_csv(incidents: list, filename: str):
    if not incidents:
        print("No venues to save.")
        return

    # Use field names from the Venue model
    fieldnames = Incident.model_fields.keys()

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(incidents)
    print(f"Saved {len(incidents)} incidents to '{filename}'.")
