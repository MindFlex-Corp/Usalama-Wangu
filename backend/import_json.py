import os
import django
import json


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Usalama_Wangu.settings")
django.setup()

from Zones.models import Zone

# Load JSON data
with open("./zones.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Create Zone objects
zones = [
    Zone(
        id=item["id"],
        type=item["type"],
        latitude=item["latitude"],
        longitude=item["longitude"],
        radius=item["radius"],
        title=item["title"],
        description=item["description"],
        timestamp=item["timestamp"],
    )
    for item in data
]

# Bulk insert
Zone.objects.bulk_create(zones, ignore_conflicts=True)
print(f"Inserted {len(zones)} records into PostgreSQL via Django ORM.")
