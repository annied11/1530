# 1530 Project
A simple Django + HTML app that surfaces University of Pittsburgh club events.  

## How to Run
### Backend (Django)
1. `cd backend`
2. `python -m venv venv && source venv/bin/activate` (Windows: `venv\Scripts\activate`)
3. `pip install -r requirements.txt`
4. `python manage.py migrate`
5. `python manage.py runserver`

Endpoints:
- `GET /` – server-rendered event list via Django template
- `GET /events/` – JSON payload powered by `data/events_sample.json`

### Frontend (Static HTML)
Open `frontend/index.html` in a browser while the backend is running on `http://localhost:8000`.  
The page fetches `/events/` and displays the list using vanilla JS.

## Structure
```
1530/
├── backend/          # Django project (campus_events + events_app)
├── frontend/         # Standalone HTML/JS page that calls /events
├── data/             # Mock datasets used by the backend
├── docs/             # Sprint notes and design docs
└── README.md         # Project overview and setup instructions
```
