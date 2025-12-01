import json
from pathlib import Path
from datetime import datetime

from django.core.management.base import BaseCommand
from django.conf import settings

from events_app.models import Event, Organization


class Command(BaseCommand):
    help = "Import events from data/events_sample.json into the database"

    def handle(self, *args, **options):
        # Match the path used in your views (BASE_DIR.parent / 'data' / 'events_sample.json')
        data_path = Path(settings.BASE_DIR).parent / "data" / "events_sample.json"

        if not data_path.exists():
            self.stderr.write(self.style.ERROR(f"File not found: {data_path}"))
            return

        with data_path.open(encoding="utf-8") as f:
            try:
                events_data = json.load(f)
            except json.JSONDecodeError as e:
                self.stderr.write(self.style.ERROR(f"JSON decode error: {e}"))
                return

        if not isinstance(events_data, list):
            self.stderr.write(self.style.ERROR("Expected a list of events in JSON."))
            return

        created_count = 0
        updated_count = 0

        for obj in events_data:
            name = (obj.get("name") or "").strip()
            org_name = (obj.get("organization") or "Unknown Organization").strip()
            location = obj.get("location") or ""
            category = obj.get("category") or ""
            external_id = str(obj.get("id")) if obj.get("id") is not None else ""

            date_str = obj.get("date")
            if not date_str:
                # Skip events with no date
                continue

            try:
                # Example format: "2025-09-10T18:00:00"
                dt = datetime.fromisoformat(date_str)
            except ValueError:
                self.stderr.write(self.style.WARNING(f"Skipping event with bad date: {date_str}"))
                continue

            # Get or create the organization
            org, _ = Organization.objects.get_or_create(name=org_name)

            # Use name + org + date as a natural key to avoid duplicates
            event, created = Event.objects.update_or_create(
                name=name,
                organization=org,
                date=dt,
                defaults={
                    "location": location,
                    "category": category,
                    "external_id": external_id,
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Import complete: {created_count} created, {updated_count} updated from {data_path}"
        ))
