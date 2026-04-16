# IRCTC Booking System

A scalable backend system inspired by the Indian Railways ticketing platform (IRCTC), designed to handle **train search, seat availability, ticket booking, PNR tracking, and user management**.

Built using **Django REST Framework**, this project demonstrates real-world backend architecture including authentication, modular API design, and complex business logic.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 4.x |
| API | Django REST Framework |
| Auth | JWT (SimpleJWT) - Access + Refresh tokens |
| Database | SQLite (dev) / PostgreSQL (prod) |
| CORS | django-cors-headers |

---

## Project Structure

```
irctc_backend/
├── irctc_backend/       # Project config (settings, urls)
├── users/               # Auth — register, login, profile
├── trains/              # Stations, Trains, Availability
│   └── management/
│       └── commands/
│           └── seed_data.py   # Load sample data
└── bookings/            # Booking, Passengers, PNR, Cancellation
```

---

## Quick Start

```bash
# 1. Install dependencies
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers

# 2. Run migrations
python manage.py migrate

# 3. Load sample data (16 stations, 10 trains, 1980 availability records)
python manage.py seed_data

# 4. Create admin
python manage.py createsuperuser

# 5. Start server
python manage.py runserver
```

---

## API Endpoints

### Auth  `/api/auth/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/register/` | Public | Register new user |
| POST | `/login/` | Public | Login → returns access + refresh JWT |
| POST | `/token/refresh/` | Public | Refresh access token |
| POST | `/logout/` | Bearer | Blacklist refresh token |
| GET/PUT | `/profile/` | Bearer | View / update profile |
| POST | `/change-password/` | Bearer | Change password |

### Trains  `/api/trains/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/stations/?q=Mumbai` | Public | Search stations by name/code/city |
| GET | `/search/?from=CSTM&to=NDLS&date=2026-05-01` | Public | Search trains with availability |
| GET | `/<train_number>/` | Public | Full train detail with stops |
| GET | `/<train_number>/availability/?date=2026-05-01` | Public | Seat availability per class |

**Train Search Parameters:**
- `from` — source station code (e.g. `CSTM`)
- `to` — destination station code (e.g. `NDLS`)
- `date` — journey date `YYYY-MM-DD`
- `class` *(optional)* — filter by `SL`, `3A`, `2A`, `1A`, `CC`
- `quota` *(optional)* — `GN`, `TK`, `PT`, `LD`, `HH`, `DF`

### Bookings  `/api/bookings/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/book/` | Bearer | Book ticket (1–6 passengers) |
| GET | `/pnr/<pnr>/` | Public | PNR status check |
| GET | `/my-bookings/` | Bearer | List user's bookings |
| GET | `/<id>/` | Bearer | Booking detail |
| POST | `/<id>/cancel/` | Bearer | Cancel booking + auto refund calc |

---

## Data Models

```
User ──────────── Booking ─────── Passenger
                     │
           ┌─────────┼───────────┐
          Train   CoachClass  Station
           │
       TrainStop (route stops)
           │
       SeatAvailability (date-wise)
```

---

## Business Logic

- **Fare Calculation**: Base fare + ₹40 reservation charge + 5% GST × passengers
- **Tatkal Quota**: Uses `tatkal_fare` field per coach class
- **Seat Allotment**: Auto-assigns coach, seat, and berth on confirmation
- **Waitlist**: Auto-promotes to waitlist when no seats available
- **Cancellation Refund Policy**:
  - 48+ hours before departure → 75% refund
  - 12–48 hours → 50% refund
  - 4–12 hours → 25% refund
  - Under 4 hours / after chart → No refund

---

## Seeded Sample Data

**Stations (16):** CSTM, NDLS, HWH, MAS, SBC, SC, ADI, PUNE, JP, LKO, PNBE, BPL, NGP, ST, BSB, AGC

**Trains (10):**
- 12301 Howrah Rajdhani Express (CSTM→NDLS)
- 12951 Mumbai Rajdhani Express (CSTM→NDLS)
- 22209 Mumbai Duronto Express (CSTM→NDLS)
- 12137 Punjab Mail (CSTM→NDLS)
- 12261 Howrah Duronto Express (CSTM→HWH)
- 12009 Mumbai Shatabdi Express (CSTM→PUNE)
- 12431 Rajdhani Express (NDLS→HWH)
- 12621 Tamil Nadu Express (NDLS→MAS)
- 12649 Karnataka Sampark Kranti (NDLS→SBC)
- 12001 Bhopal Shatabdi (NDLS→BPL)

**Availability**: 1980 records (10 trains × ~4 classes × 60 days)

---

## Admin Panel

Visit `/admin/` with superuser credentials.
Manage trains, stations, bookings, passengers, availability all from Django Admin.

---

## Production Checklist

- [ ] Switch `DEBUG = False`
- [ ] Set strong `SECRET_KEY`
- [ ] Switch to PostgreSQL in `DATABASES`
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Configure `CORS_ALLOWED_ORIGINS` (not `ALLOW_ALL`)
- [ ] Add Razorpay / PayU payment gateway integration
- [ ] Add SMS/email notifications (Twilio / SendGrid)
- [ ] Deploy with Gunicorn + Nginx
- [ ] Add Redis for caching seat availability

---

## v2.0 — New Endpoints (Services & Support)

### Services  `/api/services/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/live/<train_number>/?date=YYYY-MM-DD` | Public | Live train position, delay, stop-by-stop status |
| GET | `/platform/?station=CSTM` | Public | Platform-wise arrivals & departures |
| GET/POST | `/alerts/` | Bearer | Get / create train alerts (delay, platform change, chart) |
| DELETE | `/alerts/<id>/` | Bearer | Remove a train alert |
| GET | `/catering/menu/?station=CSTM` | Public | Catering vendors and menu by station |
| GET/POST | `/catering/orders/` | Bearer | View / place e-Catering orders |
| GET/POST | `/season-pass/` | Bearer | View / buy monthly, quarterly, half-yearly season passes |
| GET | `/tours/` | Public | All tour packages (filter: `?category=HERITAGE&max_price=15000`) |
| GET | `/tours/<id>/` | Public | Tour package detail |

### Support  `/api/support/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/ticket/` | Public | Submit a support ticket |
| GET | `/ticket/<ticket_id>/` | Public | Check ticket status + replies |
| GET | `/my-tickets/` | Bearer | All tickets for logged-in user |
| POST | `/ticket/<ticket_id>/reply/` | Bearer | Reply to an existing ticket |
| GET | `/faq/` | Public | FAQs grouped by section |

### New Seed Commands

```bash
python manage.py seed_services   # 6 vendors, 60 menu items, 6 tour packages
python manage.py seed_support    # 9 FAQs across 6 sections
```

### Full API Summary (v2.0)

| App | Endpoints | Models |
|---|---|---|
| users | 6 | User |
| trains | 4 | Station, Train, TrainStop, CoachClass, SeatAvailability |
| bookings | 5 | Booking, Passenger |
| services | 9 | LiveTrainStatus, TrainAlert, CateringVendor, MenuItem, CateringOrder, SeasonPass, TourPackage |
| support | 5 | SupportTicket, TicketReply, FAQ |
| **Total** | **29** | **17 models** |
