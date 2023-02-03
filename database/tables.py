from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, func, select
from sqlalchemy.orm import column_property, relationship

from database.database import Base


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    description = Column(String)
    price = Column(Numeric(10, 2))
    submenu_id = Column(
        Integer,
        ForeignKey(
            "submenus.id",
            ondelete="CASCADE",
        ),
        index=True,
    )
    submenu = relationship("Submenu", back_populates="dishes")


class Submenu(Base):
    __tablename__ = "submenus"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    description = Column(String)
    menu_id = Column(
        Integer,
        ForeignKey(
            "menus.id",
            ondelete="CASCADE",
        ),
        index=True,
    )
    menu = relationship("Menu", back_populates="submenus", lazy="selectin")
    dishes = relationship("Dish", back_populates="submenu")
    dishes_count = column_property(
        select(func.count(Dish.id)).filter(Dish.submenu_id == id).scalar_subquery(),
    )


class Menu(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    description = Column(String)
    submenus = relationship("Submenu", back_populates="menu", lazy="selectin")
    submenus_count = column_property(
        select(func.count(Submenu.id)).filter(Submenu.menu_id == id).scalar_subquery(),
    )
    dishes_count = column_property(
        select(func.count(Dish.id))
        .select_from(Submenu)
        .join(Submenu.dishes)
        .filter(Submenu.menu_id == id)
        .scalar_subquery(),
    )
