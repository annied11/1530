from django.test import TestCase
from django.urls import reverse
from django.conf import settings
import json
from pathlib import Path


class EventEndpointsTests(TestCase):
    def setUp(self):
        data_path = Path(settings.BASE_DIR).parent / "data" / "events_sample.json"
        with data_path.open() as fp:
            self.sample = json.load(fp)

    def test_events_api_returns_json(self):
        response = self.client.get(reverse("events_api"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), self.sample)

    def test_event_list_page_renders_data(self):
        response = self.client.get(reverse("event_list"))
        self.assertContains(response, self.sample[0]["name"])
