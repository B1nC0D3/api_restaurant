from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .database import engine

Base = declarative_base()


class BaseMenu:
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)


class Menu(BaseMenu, Base):
    __tablename__ = 'menus'

    submenus = relationship('Submenu', back_populates='menu')


class Submenu(BaseMenu, Base):
    __tablename__ = 'submenus'

    menu_id = Column(Integer, ForeignKey('menus.id', ondelete='CASCADE'), index=True)
    menu = relationship('Menu', back_populates='submenus')
    dishes = relationship('Dish', back_populates='submenu')


class Dish(BaseMenu, Base):
    __tablename__ = 'dishes'

    price = Column(Numeric(10, 2))
    submenu_id = Column(Integer, ForeignKey('submenus.id', ondelete='CASCADE'), index=True)
    submenu = relationship('Submenu', back_populates='dishes')


Base.metadata.create_all(engine)
