                 # 🚂 Train Station API

A RESTful API service for managing train stations, routes, journeys, crew, and ticket bookings. Built with Django REST Framework.

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Database Structure](#database-structure)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)

---

## ✨ Features

- Manage train stations with geolocation (latitude/longitude)
- Create and manage routes between stations
- Schedule journeys with departure and arrival times
- Assign crew members to journeys
- Book tickets with cargo and seat selection
- Order management linked to authenticated users

---

## 🛠 Tech Stack

- **Python 3.11**
- **Django 5.2**
- **Django REST Framework**
- **SQLite** (development)

---

## 🗄 Database Structure

```
Station          — name, latitude, longitude
Route            — source (Station), destination (Station), distance
TrainType        — name
Train            — name, cargo_num, places_in_cargo, train_type (TrainType)
Crew             — first_name, last_name
Journey (Trip)   — route, train, crew (M2M), departure_time, arrival_time
Order            — created_at, user (Django built-in)
Ticket           — cargo, seat, journey (Journey), order (Order)
```

### Relationships

- `Route` has one `source` and one `destination` → both are `Station`
- `Train` belongs to one `TrainType`
- `Journey` belongs to one `Route` and one `Train`, has many `Crew` members
- `Ticket` belongs to one `Journey` and one `Order`
- `Order` belongs to one `User` (Django built-in auth)

---

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/your-username/train-station-api.git
cd train-station-api

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
```

---

## 🚀 Running the Project

```bash
# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

The API will be available at: `http://localhost:8000/`

Admin panel: `http://localhost:8000/admin/`

---

## 📡 API Endpoints

| Resource     | Endpoint               | Methods                    |
|--------------|------------------------|----------------------------|
| Stations     | `/api/stations/`       | GET, POST, PUT, DELETE     |
| Routes       | `/api/routes/`         | GET, POST, PUT, DELETE     |
| Train Types  | `/api/train-types/`    | GET, POST, PUT, DELETE     |
| Trains       | `/api/trains/`         | GET, POST, PUT, DELETE     |
| Crew         | `/api/crew/`           | GET, POST, PUT, DELETE     |
| Journeys     | `/api/journeys/`       | GET, POST, PUT, DELETE     |
| Orders       | `/api/orders/`         | GET, POST                  |
| Tickets      | `/api/tickets/`        | GET, POST                  |

> Authentication is required for order and ticket endpoints.

---

## 📁 Project Structure

```
train-station-api/
├── station/                  # Main app
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── station_configs/          # Project config
│   ├── settings/
│   │   ├── __init__.py
│   │   └── base.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── requirements.txt
└── .env
```