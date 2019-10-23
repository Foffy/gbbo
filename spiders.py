import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
import json
import scrapy_items

class RecipesSpider(scrapy.Spider):
    """
    Scrape thegreatbritishbakeoff for recipes.
    Will crawl through pagination links to find recipes.
    """

    name = "recipes"

    start_urls = [
            'https://thegreatbritishbakeoff.co.uk/recipes/all/',
    ]

    def parse(self, response):

        # follow recipes
        for href in response.css('div.recipes-loop__item a::attr(href)'):
            yield response.follow(href, self.parse_recipe)

        pagination_str = response.css('div.recipes-loop__pagination')
        cur_page = pagination_str.re(r'page-numbers current">(\d)')[0]

        page_links = response.css('div.recipes-loop__pagination a::attr(href)').getall()
        next_page = str(int(cur_page) + 1)

        for link in page_links:
            if next_page in link:
                yield response.follow(link, self.parse)

    def parse_recipe(self, response):
        title = response.css('div.page-banner__title h1::text').get()
        values = response.css('.recipe-details__item .value::text').getall()
        series = response.css('.recipe-introduction__baker p::text').re(r'\d+')
        baking_time = ""
        if len(values) == 4:
            baking_time = values[3]
        if len(series) > 0:
            series = series[0]
        baker_name = response.css('.recipe-introduction__baker a::text').get()
        baker_role = response.css('.recipe-introduction__baker a::attr(href)').re('(?<=\[)(.*)\]')
        if len(baker_role) > 0:
            baker_role = baker_role[0]
        else:
            baker_role = 'none'
        baker_site_id = response.css('.recipe-introduction__baker a::attr(href)').re('\d+')
        if len(baker_site_id) > 0:
            baker_site_id = baker_site_id[0]
        else:
            baker_site_id = '0'
        recipe_instructions_raw = response.css('.recipe-instructions p::text').getall()
        recipe_steps = len(recipe_instructions_raw)
        recipe_instructions = ""
        for ins in recipe_instructions_raw:
            recipe_instructions += "{}\n".format(ins)

        ingredients = [resp.strip() for resp in response.css('.recipe-sidebar__section--ingredients p::text').getall()]
        ingredients_s = pd.Series(ingredients)

        # separate amounts, units and ingredient types
        ingredients_extract = ingredients_s.str.extract('^(?P<Amount>\d*)?\s*(?P<Unit>g|ml|tsp|tbsp)?\s*(?P<Ingredient>.*)')

        # if no amount is found, set the value to '1'. Set the column data type to int
        ingredients_extract['Amount'] = ingredients_extract['Amount'].replace('', '1')

        # set default 'unit' value if no unit value is found
        ingredients_extract['Unit'] = ingredients_extract['Unit'].fillna('unit')

        equipment = [resp.strip() for resp in response.css('.recipe-sidebar__section--equipment p::text').getall()]

        recipe_item = scrapy_items.RecipeItem()

        recipe_item['title'] = title
        recipe_item['serves'] = values[0]
        recipe_item['difficulty'] = values[1]
        recipe_item['hands_on_time'] = values[2]
        recipe_item['baking_time'] = baking_time
        recipe_item['steps'] = recipe_steps
        recipe_item['series'] = series 

        recipe_item['ingredients'] = []
        recipe_item['equipments'] = []

        recipe_baker = scrapy_items.BakerItem()
        recipe_baker['name'] = baker_name
        recipe_baker['role'] = baker_role
        recipe_baker['site_id'] = baker_site_id

        recipe_item['baker'] = recipe_baker
        recipe_item['description'] = recipe_instructions

        # convert ingredients to ingredient items
        for row in range(len(ingredients_extract)):
            ingredient_item = scrapy_items.IngredientItem()
            ingredient_item['amount'] = ingredients_extract['Amount'][row]
            ingredient_item['unit'] = ingredients_extract['Unit'][row]
            ingredient_item['ingredient'] = ingredients_extract['Ingredient'][row]
            recipe_item['ingredients'].append(ingredient_item)

        # convert equipment to equipment items
        for row in equipment:
            equipment_item = scrapy_items.EquipmentItem()
            equipment_item['equipment'] = row
            recipe_item['equipments'].append(equipment_item)

        # yield a finished item to the pipeline for further work
        yield recipe_item

def main():
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})

    settings = {}
    settings['USER_AGENT'] = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    settings['FEED_FORMAT'] = 'json'
    settings['FEED_URI'] = 'result.json'
    settings['LOG_LEVEL'] = 'WARNING'
    settings['ITEM_PIPELINES'] = {'pipelines.RecipePipeline': 100}

    process = CrawlerProcess(settings)

    process.crawl(RecipesSpider)
    process.start()


if __name__ == "__main__":
    main()
