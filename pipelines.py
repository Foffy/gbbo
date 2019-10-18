from sqlalchemy.orm import sessionmaker
import requests
import os
import alchemy_models

class RecipePipeline(object):
    def __init__(self):
        engine = alchemy_models.db_connect()
        alchemy_models.create_tables(engine)

        self.Session = sessionmaker(bind=engine)

    def add_series(self, session, series):
        # some recipes do not belong to a series, so use fake series 0
        series_num = int(series or 0)

        # get id if series already exists in database
        sql_series = session.query(alchemy_models.Series).filter_by(series_number=series_num)
        if sql_series.count() > 0:
            return sql_series[0].id
        # otherwise add new series and get id
        else:
            series_model = alchemy_models.Series()
            series_model.series_number = series_num
            try:
                session.add(series_model)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
            sql_series = session.query(alchemy_models.Series).filter_by(series_number=series_num)

        return sql_series[0].id

    def add_baker(self, session, baker):
        sql_baker = session.query(alchemy_models.Baker).filter_by(site_id=baker['site_id'])
        if sql_baker.count() > 0:
            return sql_baker[0].id
        else:
            baker_model = alchemy_models.Baker()
            baker_model.role = baker['role']
            baker_model.name = baker['name']
            baker_model.site_id = baker['site_id']
            try:
                session.add(baker_model)
                session.commit()
            except:
                session.rollback()
                raise
            sql_baker = session.query(alchemy_models.Baker).filter_by(site_id=baker['site_id'])

        return sql_baker[0].id

    def add_ingredients(self, session, item, recipe_id):
        for ingredient in item['ingredients']:
            sql_unit = session.query(alchemy_models.UnitType).filter_by(name=ingredient['unit'])
            if sql_unit.count() > 0:
                sql_unit = sql_unit[0].id
            else:
                unit_model = alchemy_models.UnitType()
                unit_model.name = ingredient['unit']
                try:
                    session.add(unit_model)
                    session.commit()
                except:
                    session.rollback()
                    raise
                sql_unit = session.query(alchemy_models.UnitType).filter_by(name=ingredient['unit'])[0].id

            sql_ingredient = session.query(alchemy_models.IngredientType).filter_by(name=ingredient['ingredient'])
            if sql_ingredient.count() > 0:
                sql_ingredient = sql_ingredient[0].id
            else:
                type_model = alchemy_models.IngredientType()
                type_model.name = ingredient['ingredient']
                try:
                    session.add(type_model)
                    session.commit()
                except:
                    session.rollback()
                    raise
                sql_ingredient = session.query(alchemy_models.IngredientType).filter_by(name=ingredient['ingredient'])[0].id

            ingredient_model = alchemy_models.Ingredient()
            ingredient_model.recipe_id = recipe_id
            ingredient_model.ingredient_type = sql_ingredient
            ingredient_model.unit_type = sql_unit
            session.add(ingredient_model)

    def add_equipment(self, session, item, recipe_id):
        for equipment in item['equipments']:
            equipment_model = alchemy_models.Equipment()
            equipment_model.name = equipment['equipment']
            equipment_model.recipe_id = recipe_id

            session.add(equipment_model)

        try:
            session.commit()
        except:
            session.rollback()
            raise

    def process_item(self, item, spider):
        """
        Callback to this for each yielded scrapy item

        """

        session = self.Session()

        # don't add a recipe that already exists in the database
        recipe_exists = session.query(alchemy_models.Recipe).filter_by(title=item['title']).count() > 0
        if recipe_exists:
            return item

        # convert from scrapy item to alchemy model
        recipe = alchemy_models.Recipe()

        recipe.title = item['title']
        recipe.serves = item['serves']
        recipe.difficulty = item['difficulty']
        recipe.hands_on_time = item['hands_on_time']
        recipe.baking_time = item['baking_time']
        recipe.steps = item['steps']

        try:
            recipe.series_id = self.add_series(session, item['series'])
            recipe.baker_id = self.add_baker(session, item['baker'])

            session.add(recipe)
            session.commit()

            recipe_id = session.query(alchemy_models.Recipe).filter_by(title=item['title'])[0].id
            self.add_ingredients(session, item, recipe_id)
            self.add_equipment(session, item, recipe_id)

            session.commit()

            print(recipe)
        except:
            session.rollback()
            raise

        finally:
            session.close()

        return item
