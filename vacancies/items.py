# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class VacanciesItem(scrapy.Item):
    company = scrapy.Field()
    title = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()
