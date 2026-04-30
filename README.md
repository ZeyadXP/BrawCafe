# ☕ Brewhaus Café — Full Stack App

A real-time café ordering system with a **FastAPI** backend and **SQLite** database.

---

## Project Structure

```
brewhaus/
├── main.py          # FastAPI app + all routes
├── database.py      # SQLAlchemy engine & session
├── models.py        # ORM models (MenuItem, Order, OrderItem)
├── schemas.py       # Pydantic schemas (request/response validation)
├── crud.py          # Database operations
├── seed.py          # Seeds default menu items
├── start.sh         # Startup script (seed + run server)
├── requirements.txt
├── Procfile         # For Railway/Heroku
├── railway.json     # Railway deployment config
├── render.yaml      # Render.com deployment config
└── static/
    └── index.html   # The full frontend (served by FastAPI)
```

---

## Run Locally

```bash
# 1. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Seed the database with default menu items
python seed.py

# 4. Start the server
uvicorn main:app --reload

# 5. Open http://localhost:8000
```

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/login` | Staff PIN login |
| GET | `/api/menu` | Get all menu items |
| POST | `/api/menu` | Add a menu item |
| PUT | `/api/menu/{id}` | Update a menu item (e.g. price) |
| DELETE | `/api/menu/{id}` | Remove a menu item |
| POST | `/api/orders` | Place a new order |
| GET | `/api/orders` | Get all active orders (staff) |
| GET | `/api/orders/{id}` | Get a specific order (tracking) |
| PUT | `/api/orders/{id}/status` | Advance order status (staff) |
| GET | `/api/stats` | Get today's stats |

Interactive API docs: `http://localhost:8000/docs`

---

## Deploy to Railway (Free)

1. Push to GitHub
2. Go to [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Select your repo
4. Set environment variable: `EMPLOYEE_PIN=your_secret_pin`
5. Done — Railway uses `railway.json` automatically

## Deploy to Render (Free)

1. Push to GitHub
2. Go to [render.com](https://render.com) → New Web Service → Connect GitHub
3. Render reads `render.yaml` automatically
4. Change `EMPLOYEE_PIN` in the Render dashboard environment variables

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `EMPLOYEE_PIN` | `1234` | Staff dashboard PIN |
| `DATABASE_URL` | `sqlite:///./brewhaus.db` | Database URL (use Postgres in production) |
| `PORT` | `8000` | Port the server listens on |

---

## Using PostgreSQL in Production

Set `DATABASE_URL` to your Postgres connection string:
```
postgresql://user:password@host:5432/dbname
```
The app handles the `postgres://` → `postgresql://` fix automatically.
