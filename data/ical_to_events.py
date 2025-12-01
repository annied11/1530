import json
from datetime import datetime, date
from pathlib import Path

from icalendar import Calendar
from icalendar.prop import vCategory

ICS_PATH = Path("ics.ics")         
JSON_PATH = Path("events_sample.json")    


def to_iso(dt):
    if isinstance(dt, datetime):
        dt_naive = dt.replace(tzinfo=None)
        return dt_naive.isoformat(timespec="seconds")  # e.g. "2025-09-10T18:00:00"

    if isinstance(dt, date):
        dt_full = datetime(dt.year, dt.month, dt.day, 0, 0, 0)
        return dt_full.isoformat(timespec="seconds")

    return None


def get_category(component):
    cats = component.get("categories")
    if not cats:
        return None

    if isinstance(cats, (list, tuple)):
        props = cats
    else:
        props = [cats]

    chosen = None

    for prop in props:
        if hasattr(prop, "to_ical"):
            raw = prop.to_ical()
        else:
            raw = prop

        if isinstance(raw, bytes):
            raw = raw.decode()

        text = str(raw).strip()

        params = getattr(prop, "params", {})
        cg_cat = params.get("X-CG-CATEGORY")

        # Prefer event_type (e.g. Recruitment, Social, Meeting, etc.)
        if cg_cat == "event_type":
            chosen = text
            break

        # Otherwise keep the first thing we see as fallback
        if chosen is None:
            chosen = text

    if not chosen:
        return None

    # Strip prefixes like "event_type:Recruitment"
    if ":" in chosen:
        chosen = chosen.split(":", 1)[-1].strip()

    # If multiple values, keep the first
    if "," in chosen:
        chosen = chosen.split(",", 1)[0].strip()

    return chosen or None


def get_organization(component):
    organizer = component.get("organizer")
    if organizer:
        cn = organizer.params.get("CN")
        if cn:
            return str(cn)

        text = str(organizer)
        if text.upper().startswith("MAILTO:"):
            return text[len("MAILTO:"):]
        return text

    category = get_category(component)
    if category:
        return category
    return "University of Pittsburgh"


def main():
    ics_bytes = ICS_PATH.read_bytes()
    cal = Calendar.from_ical(ics_bytes)

    events = []

    for idx, component in enumerate(cal.walk("VEVENT"), start=1):
        summary = str(component.get("summary", "")).strip()
        dtstart = component.get("dtstart")
        location = str(component.get("location", "")).strip() or None
        category = get_category(component)
        organization = get_organization(component)

        date_str = None
        if dtstart:
            date_str = to_iso(dtstart.dt)

        event_obj = {
            "id": idx,
            "name": summary,
            "organization": organization,
            "location": location,
            "date": date_str,
            "category": category,
        }
        events.append(event_obj)

    # --- NEW: sort events by date (earliest first) ---
    def sort_key(ev):
        d = ev.get("date")
        if not d:
            # push missing dates to the end
            return datetime.max
        return datetime.fromisoformat(d)

    events.sort(key=sort_key)
    # --- END NEW ---

    JSON_PATH.write_text(
        json.dumps(events, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    print(f"Wrote {len(events)} events to {JSON_PATH}")


if __name__ == "__main__":
    main()
