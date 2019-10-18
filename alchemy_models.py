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

    role = Column(Integer, ForeignKey('role_type.id'))
    name = Column('name', String)
    site_id = Column('site_id', Integer)

    # a baker can have several recipes
    recipes = relationship('Recipe', back_populates='baker') 

class Recipe(Base):
    __tablename__ = 'recipe'
    id = Column(Integer, primary_key=True)

    title = Column('title', String)

    # a recipe should be connected to only one baker
    baker_id = Column(Integer, ForeignKey('baker.id'))
    baker = relationship('Baker', back_populates='recipes')

    serves = Column('serves', String)
    difficulty = Column('difficulty', String)
    hands_on_time = Column('hands_on_time_amount', String)
    baking_time = Column('baking_time', String)
    recipe_steps = Column('recipe_steps', Integer)
    description = Column('description', String)

    # a recipe should be connected to only one series
    series_id = Column(Integer, ForeignKey('series.id'))
    series = relationship('Series', back_populates="recipes")

    # a recipe can have several ingredients and equipments
    ingredients = relationship('Ingredient', back_populates="recipe")
    equipments = relationship('Equipment', back_populates="recipe")

    def __repr__(self):
        return "Recipe {:}: {:}\nBaker name: {:}, Role: {:}, site id: {:}\nServes: {:}\nDifficulty: {:}\nHands on time: {:}\nBaking time: {:}\nSteps: {:}\nIngredients: {:}\nEquipment: {:}\nSeries: {:}\n\n".format(
                self.id,
                self.title,
                self.baker.name,
                self.baker.role,
                self.baker.site_id,
                self.serves,
                self.difficulty,
                self.hands_on_time,
                self.baking_time,
                self.steps,
                len(self.ingredients),
                len(self.equipments),
                self.series.series_number)

class Ingredient(Base):
    __tablename__ = 'ingredient'
    id = Column(Integer, primary_key=True)

    # a certain ingredient is connected to a single recipe
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    recipe = relationship('Recipe', back_populates="ingredients")

    amount = Column('amount', Float())
    ingredient_type = Column(Integer, ForeignKey('ingredient_type.id'))
    unit_type = Column(Integer, ForeignKey('unit_type.id'))

class Equipment(Base):
    __tablename__ = 'equipment'
    id = Column(Integer, primary_key=True)

    # a certain equipment is connected to a single recipe
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    recipe = relationship('Recipe', back_populates="equipments")

    name = Column('name', String)

class IngredientType(Base):
    __tablename__ = 'ingredient_type'
    id = Column(Integer, primary_key=True)

    name = Column('name', String)

class UnitType(Base):
    __tablename__ = 'unit_type'
    id = Column(Integer, primary_key=True)

    name = Column('name', String)

class RoleType(Base):
    __tablename__ = 'role_type'
    id = Column(Integer, primary_key=True)

    role = Column('role', String)

class Series(Base):
    __tablename__ = 'series'
    id = Column(Integer, primary_key=True)

    series_number = Column('series_number', Integer)

    # point to the winning recipe
    winner = Column(Integer, ForeignKey('baker.id'))

    # many recipes per series
    recipes = relationship('Recipe', back_populates='series') 

if __name__ == "__main__":
    engine = db_connect()
    create_tables(engine)
