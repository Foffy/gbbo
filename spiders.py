import json
import scrapy
import scrapy
from scrapy import CrawlerProcess
from scrapy.utils.log import configure_logging
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
        labels = response.css('div.recipe-details__item').re(r'label">(\w+)')
        values = response.css('div.recipe-details__item').re(r'value">(\w+)')


        with open('../snakemake/outputmappe/recipes.txt', 'a+') as f:
            f.write("{}\n".format(title))
