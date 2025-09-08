# 🚖 Cab Booking Backend (FastAPI + MySQL + MongoDB)

This is the backend system for a cab booking application — similar to Uber/Ola — built using **FastAPI**, **MySQL**, and **MongoDB**.

It supports two separate apps:
- 👤 **User app** — for customers booking rides
- 🚗 **Driver app** — for drivers accepting rides

The backend supports:
- Full CRUD for users, drivers, trips, payments, feedback, subscriptions, and referrals
- MongoDB collections for trip logs, search history, and live trip updates
- Ready-to-use RESTful APIs (testable via Postman or Swagger)

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
2. Create a Virtual Environment
```bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install Dependencies
```bash

pip install -r requirements.txt
```
🗂 Project Structure (Simplified)
``` bash

app/
├── models/           # SQLAlchemy models (MySQL)
├── models_mongo/     # MongoDB schemas (Pydantic)
├── schemas/          # Pydantic schemas for API validation (MySQL)
├── schemas_mongo/    # Pydantic schemas for MongoDB collections
├── crud/             # Database operations (MySQL)
├── routes/           # FastAPI route handlers
├── database/
│   ├── mysql.py      # MySQL connection
│   └── mongo.py      # MongoDB (local or Atlas)
└── main.py           # FastAPI entrypoint

```

🚀 Running the App (Locally)
```bash

uvicorn app.main:app --reload
```
Visit:
Swagger UI: http://localhost:8000/docs



🧪 Postman Testing
All APIs follow RESTful structure

Start with creating roles → users → drivers → trips → etc.


MongoDB APIs (trip logs, search, live-trip) can be tested independently



📦 Databases
MySQL — handles structured data (users, trips, etc.)

MongoDB — used for GPS tracking, search logs, live updates

Redis — optional for caching (not configured yet)
