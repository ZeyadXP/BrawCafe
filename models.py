from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class MenuItem(Base):
    __tablename__ = "menu_items"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    emoji       = Column(String, default="🍽️")
    category    = Column(String, nullable=False)
    price       = Column(Float, nullable=False)
    description = Column(String, default="")
    is_new      = Column(Boolean, default=False)
    created_at  = Column(DateTime, default=datetime.utcnow)


class Order(Base):
    __tablename__ = "orders"

    id          = Column(String, primary_key=True, index=True)   # e.g. "#4823"
    customer    = Column(String, nullable=False)
    status      = Column(String, default="new")                  # new | preparing | ready | done
    total       = Column(Float, nullable=False)
    placed_at   = Column(DateTime, default=datetime.utcnow)
    updated_at  = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    history     = Column(JSON, default=list)                     # [{status, time}]

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


class OrderItem(Base):
    __tablename__ = "order_items"

    id       = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, ForeignKey("orders.id"), nullable=False)
    item_id  = Column(Integer, nullable=False)
    name     = Column(String, nullable=False)
    emoji    = Column(String, default="🍽️")
    price    = Column(Float, nullable=False)
    qty      = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
