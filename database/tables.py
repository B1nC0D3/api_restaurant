from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from database.database import Base


class BaseMenu:
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    description = Column(String)


class Dish(BaseMenu, Base):
    __tablename__ = 'dishes'

    id = Column(Integer, primary_key=True)
    price = Column(Numeric(10, 2))
    submenu_id = Column(Integer, ForeignKey('submenus.id', ondelete='CASCADE'), index=True)
    submenu = relationship('Submenu', back_populates='dishes', lazy='joined')


class Submenu(BaseMenu, Base):
    __tablename__ = 'submenus'

    id = Column(Integer, primary_key=True)
    menu_id = Column(Integer, ForeignKey('menus.id', ondelete='CASCADE'), index=True)
    menu = relationship('Menu', back_populates='submenus', lazy='joined')
    dishes = relationship('Dish', back_populates='submenu',
                          lazy='joined', cascade='all, delete, delete-orphan')


class Menu(BaseMenu, Base):
    __tablename__ = 'menus'

    submenus = relationship('Submenu', back_populates='menu',
                            lazy='joined', cascade='all, delete, delete-orphan')
