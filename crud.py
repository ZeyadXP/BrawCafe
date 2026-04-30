from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
import random

from models import MenuItem, Order, OrderItem
from schemas import (
    MenuItemCreate, MenuItemUpdate,
    OrderCreate, StatsOut, PopularItem
)


# ── Menu ───────────────────────────────────────────────────────────────────────
def get_menu_items(db: Session):
    return db.query(MenuItem).order_by(MenuItem.id).all()


def create_menu_item(db: Session, item: MenuItemCreate):
    db_item = MenuItem(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_menu_item(db: Session, item_id: int, update: MenuItemUpdate):
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not db_item:
        return None
    for field, value in update.model_dump(exclude_unset=True).items():
        setattr(db_item, field, value)
    db.commit()
    db.refresh(db_item)
    return db_item


def delete_menu_item(db: Session, item_id: int):
    db_item = db.query(MenuItem).filter(MenuItem.id == item_id).first()
    if not db_item:
        return False
    db.delete(db_item)
    db.commit()
    return True


# ── Orders ─────────────────────────────────────────────────────────────────────
def _generate_order_id():
    return "#" + str(random.randint(1000, 9999))


def create_order(db: Session, order: OrderCreate):
    # Generate unique ID
    order_id = _generate_order_id()
    while db.query(Order).filter(Order.id == order_id).first():
        order_id = _generate_order_id()

    total = sum(i.price * i.qty for i in order.items)
    now   = datetime.utcnow()

    db_order = Order(
        id       = order_id,
        customer = order.customer or "Guest",
        status   = "new",
        total    = total,
        placed_at= now,
        history  = [{"status": "new", "time": now.isoformat()}],
    )
    db.add(db_order)
    db.flush()  # get the ID before adding items

    for item in order.items:
        db_item = OrderItem(
            order_id = order_id,
            item_id  = item.item_id,
            name     = item.name,
            emoji    = item.emoji,
            price    = item.price,
            qty      = item.qty,
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: str):
    return db.query(Order).filter(Order.id == order_id).first()


def get_active_orders(db: Session):
    return (
        db.query(Order)
        .filter(Order.status != "done")
        .order_by(Order.placed_at)
        .all()
    )


def get_all_orders(db: Session):
    return db.query(Order).order_by(Order.placed_at.desc()).all()


def update_order_status(db: Session, order_id: str, new_status: str):
    valid_statuses = {"new", "preparing", "ready", "done"}
    if new_status not in valid_statuses:
        return None

    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        return None

    now = datetime.utcnow()
    db_order.status     = new_status
    db_order.updated_at = now

    history = list(db_order.history or [])
    history.append({"status": new_status, "time": now.isoformat()})
    db_order.history = history

    db.commit()
    db.refresh(db_order)
    return db_order


# ── Stats ──────────────────────────────────────────────────────────────────────
def get_stats(db: Session) -> StatsOut:
    today_start = datetime.combine(date.today(), datetime.min.time())

    all_orders_today = (
        db.query(Order)
        .filter(Order.placed_at >= today_start)
        .all()
    )

    completed = [o for o in all_orders_today if o.status == "done"]
    revenue   = sum(o.total for o in completed)
    avg_order = revenue / len(completed) if completed else 0.0

    # Popular items: count qty across all today's orders
    freq: dict[str, int] = {}
    for order in all_orders_today:
        for item in order.items:
            freq[item.name] = freq.get(item.name, 0) + item.qty

    popular = sorted(
        [PopularItem(name=n, count=c) for n, c in freq.items()],
        key=lambda x: x.count,
        reverse=True
    )[:6]

    menu_count = db.query(func.count(MenuItem.id)).scalar()

    return StatsOut(
        orders_today  = len(all_orders_today),
        revenue       = revenue,
        menu_items    = menu_count,
        avg_order     = avg_order,
        popular_items = popular,
    )
