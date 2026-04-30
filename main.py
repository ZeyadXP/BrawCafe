from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from pathlib import Path
import os

from database import SessionLocal, engine, Base
from models import MenuItem, Order, OrderItem
from schemas import (
    MenuItemCreate, MenuItemUpdate, MenuItemOut,
    OrderCreate, OrderOut, OrderStatusUpdate,
    StatsOut, LoginRequest
)
import crud

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Brewhaus Café API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (the frontend HTML)
app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Serve frontend ─────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    html_path = Path("static/index.html")
    if html_path.exists():
        return HTMLResponse(content=html_path.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Place index.html in /static/</h1>")


# ── AUTH ───────────────────────────────────────────────────────────────────────
EMPLOYEE_PIN = os.environ.get("EMPLOYEE_PIN", "1234")

@app.post("/api/auth/login")
def login(req: LoginRequest):
    if req.pin == EMPLOYEE_PIN:
        return {"success": True, "message": "Access granted"}
    raise HTTPException(status_code=401, detail="Incorrect PIN")


# ── MENU ───────────────────────────────────────────────────────────────────────
@app.get("/api/menu", response_model=list[MenuItemOut])
def get_menu(db: Session = Depends(get_db)):
    return crud.get_menu_items(db)


@app.post("/api/menu", response_model=MenuItemOut)
def add_menu_item(item: MenuItemCreate, db: Session = Depends(get_db)):
    return crud.create_menu_item(db, item)


@app.put("/api/menu/{item_id}", response_model=MenuItemOut)
def update_menu_item(item_id: int, update: MenuItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_menu_item(db, item_id, update)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.delete("/api/menu/{item_id}")
def delete_menu_item(item_id: int, db: Session = Depends(get_db)):
    success = crud.delete_menu_item(db, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"success": True}


# ── ORDERS ─────────────────────────────────────────────────────────────────────
@app.post("/api/orders", response_model=OrderOut)
def place_order(order: OrderCreate, db: Session = Depends(get_db)):
    return crud.create_order(db, order)


@app.get("/api/orders", response_model=list[OrderOut])
def get_orders(db: Session = Depends(get_db)):
    """Staff: get all non-completed orders"""
    return crud.get_active_orders(db)


@app.get("/api/orders/all", response_model=list[OrderOut])
def get_all_orders(db: Session = Depends(get_db)):
    """Staff: get all orders including completed"""
    return crud.get_all_orders(db)


@app.get("/api/orders/{order_id}", response_model=OrderOut)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = crud.get_order(db, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.put("/api/orders/{order_id}/status", response_model=OrderOut)
def update_order_status(order_id: str, update: OrderStatusUpdate, db: Session = Depends(get_db)):
    order = crud.update_order_status(db, order_id, update.status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


# ── STATS ──────────────────────────────────────────────────────────────────────
@app.get("/api/stats", response_model=StatsOut)
def get_stats(db: Session = Depends(get_db)):
    return crud.get_stats(db)
