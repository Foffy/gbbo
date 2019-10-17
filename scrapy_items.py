import scrapy

class RecipeItem(scrapy.Item):
    title = scrapy.Field()

    serves = scrapy.Field()
    difficulty = scrapy.Field()
    hands_on_time = scrapy.Field()
    baking_time = scrapy.Field()

    ingredients = scrapy.Field()
    equipments = scrapy.Field()

    baker = scrapy.Field()
    steps = scrapy.Field()
    series = scrapy.Field()

class IngredientItem(scrapy.Item):
    amount = scrapy.Field()
    unit = scrapy.Field()
    ingredient = scrapy.Field()

class EquipmentItem(scrapy.Item):
    equipment = scrapy.Field()

class BakerItem(scrapy.Item):
    baker = scrapy.Field()
    role = scrapy.Field()


if __name__ == "__main__":
    baker = BakerItem(baker='John Smith')

    recipe = RecipeItem(title="John's cookie", serves="4")
    i1 = IngredientItem(amount="4", unit="tsp", ingredient="sugar")
    i2 = IngredientItem(amount="3", unit="liter", ingredient="water")

    recipe['ingredients'] = [i1, i2]
    recipe['baker'] = baker

    print(recipe)
