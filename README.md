# Train Station API 🚂

A Django REST Framework API for managing train tickets, routes, trips, and orders. This project demonstrates modern backend development practices with JWT authentication, filtering, serialization, and comprehensive API documentation.

## 📋 Project Overview

Train Station API is a fully functional REST API that allows users to:
- Browse train stations and routes
- View available trips and their schedules
- Purchase train tickets
- Manage orders with multiple tickets
- Access detailed trip information with seat availability

### Key Features

✅ **JWT Authentication** - Secure token-based authentication with refresh tokens
✅ **Admin Panel** - Full Django admin interface for managing data
✅ **API Documentation** - Interactive Swagger/OpenAPI documentation at `/api/doc/swagger/`
✅ **Advanced Filtering** - Filter trains, stations, routes, and trips
✅ **Order Management** - Create, retrieve, and manage orders with tickets
✅ **Image Uploads** - Upload station images with automatic path generation
✅ **Permission Classes** - Role-based access control (user vs admin)
✅ **Database Constraints** - Unique constraints on tickets to prevent double bookings
✅ **Comprehensive Validation** - Custom validators for trips, routes, and tickets

---

## 🛠️ Tech Stack

- **Backend**: Django 5.2.11, Django REST Framework 3.16.1
- **Database**: PostgreSQL 15
- **Authentication**: JWT (djangorestframework-simplejwt)
- **API Documentation**: drf-spectacular 0.29.0
- **Filtering**: django-filter 25.2
- **Image Processing**: Pillow 12.1.1
- **Environment**: python-dotenv 1.2.2

---

## 📦 Installation & Setup

### Prerequisites

- Python 3.11+
- PostgreSQL 15
- pip and virtualenv

### Step 1: Clone and Setup Virtual Environment

```bash
git clone https://github.com/yourusername/train-station-api.git
cd train-station-api
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Setup PostgreSQL Database

```bash
# Start PostgreSQL service
brew services start postgresql@15  # On macOS

# Create database user and database
psql -U postgres -c "CREATE USER station_user WITH PASSWORD 'station_pass';"
psql -U postgres -c "CREATE DATABASE station OWNER station_user;"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE station TO station_user;"
```

### Step 4: Configure Environment Variables

Create `.env` file in the project root:

```env
DB_HOST=localhost
DB_NAME=station
DB_USER=station_user
DB_PASSWORD=station_pass
DB_PORT=5432

SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### Step 5: Run Migrations

```bash
python manage.py migrate
```

### Step 6: Create Superuser (Admin)

```bash
python manage.py createsuperuser
# Follow prompts to create admin account
```

### Step 7: Start Development Server

```bash
python manage.py runserver
```

Server will be available at `http://127.0.0.1:8000/`

---

## 🐳 Running with Docker

### Prerequisites

- Docker and Docker Compose installed

### Steps

```bash
# Build and start containers
docker compose up --build

# Run migrations (in another terminal)
docker compose exec app python manage.py migrate

# Create superuser
docker compose exec app python manage.py createsuperuser
```

---

## 📚 API Documentation

### Interactive Swagger Documentation

Visit `http://127.0.0.1:8000/api/doc/swagger/` to explore the API interactively.

### Key Endpoints

#### Authentication
- `POST /register/` - Register new user
- `POST /login/` - Get access token
- `POST /token/refresh/` - Refresh access token
- `POST /logout/` - Logout and blacklist token
- `GET /me/` - Get current user info
- `POST /me/change-password/` - Change password

#### Train Management
- `GET /api/train-types/` - List all train types
- `GET /api/trains/` - List all trains with pagination
- `GET /api/trains/{id}/` - Get train details

#### Stations & Routes
- `GET /api/stations/` - List all stations
- `POST /api/stations/{id}/upload-image/` - Upload station image
- `GET /api/routes/` - List routes with filtering
- `GET /api/routes/?source_id=1&destination_id=2` - Filter routes

#### Trips
- `GET /api/trips/` - List all trips with available seats
- `GET /api/trips/{id}/` - Get trip details with taken seats
- `GET /api/trips/?departure_date=2024-03-10` - Filter by date

#### Crew
- `GET /api/crews/` - List all crew members
- `POST /api/crews/` - Create new crew member (admin only)

#### Orders & Tickets
- `GET /api/orders/` - Get user's orders (users see only their own)
- `POST /api/orders/` - Create new order with tickets
- `GET /api/orders/{id}/` - Get order details with tickets
- `PATCH /api/orders/{id}/` - Update order (admin only)
- `DELETE /api/orders/{id}/` - Delete order (admin only)

---

## 🔐 Authentication

### Getting Access Token

1. Register a new user:
```bash
curl -X POST http://127.0.0.1:8000/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username":"john",
    "email":"john@example.com",
    "password":"secure123",
    "password2":"secure123"
  }'
```

2. Get access token:
```bash
curl -X POST http://127.0.0.1:8000/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"secure123"}'
```

3. Use token in requests:
```bash
curl -X GET http://127.0.0.1:8000/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 📊 Database Models

### Core Models

**Station**
- name, latitude, longitude, image
- Upload station images for branding

**Route**
- source (FK to Station), destination (FK to Station), distance
- Validates that source ≠ destination

**Train**
- name, cargo_num, places_in_cargo, train_type (FK)
- Calculates total capacity: `cargo_num × places_in_cargo`

**Trip**
- departure_time, arrival_time, route (FK), train (FK)
- many-to-many relationship with Crew
- Validates departure_time < arrival_time

**Ticket**
- cargo, seat, trip (FK), order (FK)
- Unique constraint: (cargo, seat, trip) prevents double bookings
- Validates cargo and seat numbers against train specs

**Order**
- created_at, user (FK)
- Contains multiple tickets

**Crew**
- first_name, last_name
- Can be assigned to multiple trips

**TrainType**
- name (e.g., "Express", "Regional", "Freight")

---



## 🔍 Advanced Features

### Filtering & Search

```bash
# Filter trains by type
GET /api/trains/?train_type=1

# Filter routes by source and destination
GET /api/routes/?source_id=1&destination_id=2

# Filter trips by date
GET /api/trips/?departure_date=2024-03-15

# Pagination
GET /api/trains/?page=1&page_size=10
```

### Serializers

- **StationSerializer** - Basic station info
- **RouteSerializer** - Routes with station names and IDs
- **TrainListSerializer** - Trains with URLs and type names
- **TrainDetailSerializer** - Full train details
- **TripListSerializer** - Trips with available seat count
- **TripDetailSerializer** - Trip details with taken seats layout
- **OrderSerializer** - Order with nested tickets
- **OrderListSerializer** - Order list view with full ticket details

### Permission Classes

- **IsAuthenticatedOrReadOnly** - Default for all endpoints
  - Unauthenticated users can only READ (GET)
  - Authenticated users can READ and WRITE (POST, PUT, DELETE)
- **IsAuthenticated** - Required for orders
- **IsAdminUser** - Required for order updates/deletes
- Staff users can see all orders; regular users see only their own

---

## 📝 Project Structure

```
train-station-api/
├── station/                    # Main app
│   ├── models.py              # Database models
│   ├── serializers.py         # DRF serializers
│   ├── views.py               # ViewSets
│   ├── filters.py             # Custom filters
│   ├── migrations/            # Database migrations
│   └── tests.py               # Unit tests
├── user/                       # User app (if exists)
├── station_configs/           # Project settings
│   ├── settings.py            # Django settings
│   ├── urls.py                # URL routing
│   └── wsgi.py                # WSGI config
├── .env                        # Environment variables
├── .gitignore
├── requirements.txt           # Python dependencies
├── docker-compose.yml         # Docker configuration
├── Dockerfile                 # Docker image
└── README.md
```

---

## 📖 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Happy coding! 🚀**