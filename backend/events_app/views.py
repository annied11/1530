from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q
from .models import Event


def load_events(org=None, category=None, search=None):
    qs = Event.objects.select_related("organization").order_by("date")

    if org:
        qs = qs.filter(organization__name__icontains=org)

    if category:
        qs = qs.filter(category__icontains=category)

    if search:
        qs = qs.filter(
            Q(name__icontains=search) |
            Q(organization__name__icontains=search)
        )

    if not qs.exists() and not (org or category or search):
        return {
            "error": "No events available in the database.",
            "events": [],
        }

    events = []
    for event in qs:
        events.append({
            "id": event.id,
            "name": event.name,
            "organization": event.organization.name if hasattr(event, "organization") else "",
            "location": event.location,
            "date": event.date.isoformat(timespec="seconds") if event.date else None,
            "category": event.category,
        })

    return {"events": events}


def events_api(request):
    org = request.GET.get("org")
    category = request.GET.get("category")
    search = request.GET.get("q")

    result = load_events(org=org, category=category, search=search)

    if "error" in result and not result["events"]:
        response = JsonResponse(result, status=500)
    else:
        response = JsonResponse(result["events"], safe=False)

    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
    response["Vary"] = "Origin"

    return response


def event_list_page(request):
    result = load_events()
    events = result.get("events", [])
    error = result.get("error")

    return render(request, "events_app/index.html", {
        "events": events,
        "error": error,
    })
