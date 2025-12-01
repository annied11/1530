from django.http import JsonResponse
from django.shortcuts import render

from .models import Event   # <-- NEW: import your model


def load_events():
    """Load events from the database with basic error handling."""

    qs = Event.objects.select_related("organization").order_by("date")

    # Empty DB – mimic your previous error style
    if not qs.exists():
        return {
            "error": "No events available in the database. Did you run the import?",
            "events": [],
        }

    events = []
    for event in qs:
        events.append({
            "id": event.id,
            "name": event.name,
            "organization": event.organization.name if hasattr(event, "organization") else "",
            "location": event.location,
            # Match your JSON datetime format "2025-09-10T18:00:00"
            "date": event.date.isoformat(timespec="seconds") if event.date else None,
            "category": event.category,
        })

    return {"events": events}


def events_api(request):
    """Return JSON API response, now backed by the DB."""
    result = load_events()

    if "error" in result and not result["events"]:
        # Keep your old pattern: errors → 500 with a message
        response = JsonResponse(result, status=500)
    else:
        response = JsonResponse(result["events"], safe=False)

    # CORS headers as before
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Vary"] = "Origin"

    return response


def event_list_page(request):
    """Render template for the HTML page."""
    result = load_events()
    events = result.get("events", [])
    error = result.get("error")

    return render(request, "events_app/index.html", {
        "events": events,
        "error": error,
    })
