# 🏢 Meeting Room Booking System

A Backend Services for managing meeting room reservations.

Built with:

- 🔧 Backend: Django + Django REST Framework
- 🗄️ Database: MySQL

---

# 🚀 Features

- 📋 View available rooms
- 📅 Check room availability (time slots)
- 📝 Create booking
- ❌ Cancel booking
- 📊 Pagination (rooms & bookings)
- ⏱️ Time-based conflict validation

# ⚙️ Backend Setup (Django)

## 1. Buat virtual environment

```
python -m venv venv
```

### Windows:

```
venv\Scripts\activate
```

### Mac/Linux:

```
source venv/bin/activate
```

---

## 2. Install dependencies

```
pip install -r requirements.txt
```

---

## 3. Setup environment variables

Buat file `.env`:

```
DB_NAME=your_db_name
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=host
DB_PORT=port
```

---

## 4. Migrate database

```
python manage.py migrate
```

---

## 5. Run server

```
python manage.py runserver
```

---

# 🌐 API Endpoints

## Rooms

- `GET /rooms/` → list (paginated)
- `GET /rooms/all/` → all rooms (for dropdown)
- `GET /rooms/{id}/availability/?date=YYYY-MM-DD`

## Bookings

- `GET /bookings/?user={id}`
- `POST /bookings/`
- `DELETE /bookings/{id}/`

## Check details of it on

- MRoom Booking.postman_collection.json

---

# ⚠️ Important Notes

- Jangan commit `.env`
- Gunakan `.env.example` untuk referensi
- Pastikan MySQL sudah running

---

# 👨‍💻 Author

Built for learning & practice 🚀
