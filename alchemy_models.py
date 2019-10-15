from sqlalchemy import create_engine, Table, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer,
    SmallInteger,
    String,
    Date,
    DateTime,
    Float,
    Boolean,
    Text,
    LargeBinary)

Base = declarative_base()

def db_connect():
    connect_string = 'sqlite:///database.db'

    return create_engine(connect_string)


def create_tables(engine):
    Base.metadata.create_all(engine)

class Baker(Base):
    __tablename__ = 'baker'
    id = Column(Integer, primary_key=True)

    role = Column('role', String)

    # a baker can have several recipes
    recipes = relationship('Recipe', back_populates='baker') 

class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(Integer, primary_key=True)

    title = Column('title', String)

    # a recipe should be connected to only one baker
    baker_id = Column(Integer, ForeignKey('baker.id'))
    baker = relationship('Baker', back_populates='recipes')

    serves = Column('serves', Integer)
    difficulty = Column('difficulty', String)
    hands_on_time_amount = Column('hands_on_time_amount', Float)
    hands_on_time_unit = Column(Integer, ForeignKey('unit_type.id'))
    steps = Column('steps', Integer)
    description = Column('description', String)

    # a recipe can have several ingredients and equipments
    ingredients = relationship('Ingredient', back_populates='recipe')
    equipements = relationship('Equipment', back_populates='recipe')

class Ingredient(Base):
    __tablename__ = 'ingredient'
    id = Column(Integer, primary_key=True)

    # a certain ingredient is connected to a single recipe
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    recipe = relationship('Recipe', back_populates='ingredients')

    amount = Column('amount', Float())
    ingredient_type = Column(Integer, ForeignKey('ingredient_type.id'))

class Equipment(Base):
    __tablename__ = 'equipment'
    id = Column(Integer, primary_key=True)

    # a certain equipment is connected to a single recipe
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    recipe = relationship('Recipe', back_populates='equipments')

    name = Column('name', String)

class IngredientType(Base):
    __tablename__ = 'ingredient_type'
    id = Column(Integer, primary_key=True)

    name = Column('name', String)

class UnitType(Base):
    __tablename__ = 'unit_type'
    id = Column(Integer, primary_key=True)

    name = Column('name', String)


if __name__ == "__main__":
    engine = db_connect()
    create_tables(engine)
