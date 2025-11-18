import json
from pathlib import Path
from django.http import JsonResponse
from django.shortcuts import render

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR.parent / "data" / "events_sample.json"


def load_events():
    """Load events safely with error handling."""
    # Missing file
    if not DATA_FILE.exists():
        return {
            "error": "Event data file not found.",
            "events": []
        }

    try:
        with DATA_FILE.open() as fp:
            data = json.load(fp)

        # Improper JSON structure
        if not isinstance(data, list):
            return {
                "error": "Event data is improperly formatted.",
                "events": []
            }

        # Empty list
        if len(data) == 0:
            return {
                "error": "No events available.",
                "events": []
            }

        # Success
        return {
            "events": data
        }

    except json.JSONDecodeError:
        return {
            "error": "JSON file could not be parsed.",
            "events": []
        }


def events_api(request):
    """Return JSON API response."""
    result = load_events()

    # If error, return structured error
    if "error" in result:
        response = JsonResponse(result, status=500)
    else:
        response = JsonResponse(result["events"], safe=False)

    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Vary"] = "Origin"

    return response


def event_list_page(request):
    """Render template for the HTML page."""
    result = load_events()
    events = result["events"] if "events" in result else []
    error = result.get("error")

    return render(request, "events_app/index.html", {
        "events": events,
        "error": error
    })
