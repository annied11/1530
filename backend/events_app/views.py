import json
from pathlib import Path
from django.http import JsonResponse
from django.shortcuts import render

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR.parent / "data" / "events_sample.json"


def load_events():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open() as fp:
        return json.load(fp)


def events_api(request):
    events = load_events()
    response = JsonResponse(events, safe=False)
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Vary"] = "Origin"
    return response


def event_list_page(request):
    events = load_events()
    return render(request, "events_app/index.html", {"events": events})
