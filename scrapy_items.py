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
    description = scrapy.Field()
    series = scrapy.Field()

class IngredientItem(scrapy.Item):
    amount = scrapy.Field()
    unit = scrapy.Field()
    ingredient = scrapy.Field()

class EquipmentItem(scrapy.Item):
    equipment = scrapy.Field()

class BakerItem(scrapy.Item):
    name = scrapy.Field()
    role = scrapy.Field()
    site_id = scrapy.Field()
