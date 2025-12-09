from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Organization, Event


class EventsApiDbTests(TestCase):
    def setUp(self):
        # Create test organization and event in the test DB
        self.org = Organization.objects.create(
            name="CSSA",
            description="Chinese Students and Scholars Association",
            website="https://example.com/cssa",
        )

        self.event = Event.objects.create(
            name="Welcome Party",
            organization=self.org,
            location="William Pitt Union",
            date=timezone.now(),
            category="social",
        )

    def test_events_api_returns_db_events(self):
        """API returns DB-backed JSON event list."""
        url = reverse("events_api")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data), 1)

        event_json = data[0]
        self.assertEqual(event_json["name"], self.event.name)
        self.assertEqual(event_json["organization"], self.org.name)
        self.assertEqual(event_json["location"], self.event.location)
        self.assertEqual(event_json["category"], self.event.category)
        self.assertIn("date", event_json)

    def test_event_list_page_renders_event(self):
        """HTML event list page renders DB-backed event."""
        url = reverse("event_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.event.name)
        self.assertContains(response, self.org.name)
        self.assertContains(response, self.event.location)

    def test_events_api_handles_empty_database(self):
        """API returns error structure if no events exist."""
        Event.objects.all().delete()
        Organization.objects.all().delete()

        url = reverse("events_api")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 500)

        payload = response.json()
        self.assertIn("error", payload)
        self.assertIn("events", payload)
        self.assertEqual(payload["events"], [])