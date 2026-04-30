from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


# ── Auth ───────────────────────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    pin: str


# ── Menu ───────────────────────────────────────────────────────────────────────
class MenuItemCreate(BaseModel):
    name:        str
    emoji:       str = "🍽️"
    category:    str
    price:       float = Field(gt=0)
    description: str = ""
    is_new:      bool = False


class MenuItemUpdate(BaseModel):
    name:        Optional[str]   = None
    emoji:       Optional[str]   = None
    category:    Optional[str]   = None
    price:       Optional[float] = None
    description: Optional[str]   = None
    is_new:      Optional[bool]  = None


class MenuItemOut(BaseModel):
    id:          int
    name:        str
    emoji:       str
    category:    str
    price:       float
    description: str
    is_new:      bool

    model_config = {"from_attributes": True}


# ── Orders ─────────────────────────────────────────────────────────────────────
class CartItemIn(BaseModel):
    item_id: int
    name:    str
    emoji:   str
    price:   float
    qty:     int = Field(ge=1)


class OrderCreate(BaseModel):
    customer: str
    items:    list[CartItemIn]


class OrderItemOut(BaseModel):
    id:    int
    name:  str
    emoji: str
    price: float
    qty:   int

    model_config = {"from_attributes": True}


class OrderOut(BaseModel):
    id:         str
    customer:   str
    status:     str
    total:      float
    placed_at:  datetime
    updated_at: datetime
    history:    list
    items:      list[OrderItemOut]

    model_config = {"from_attributes": True}


class OrderStatusUpdate(BaseModel):
    status: str  # new | preparing | ready | done


# ── Stats ──────────────────────────────────────────────────────────────────────
class PopularItem(BaseModel):
    name:  str
    count: int


class StatsOut(BaseModel):
    orders_today:  int
    revenue:       float
    menu_items:    int
    avg_order:     float
    popular_items: list[PopularItem]
