# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from email.mime import image
from turtle import title
import scrapy


class EventbriteItem(scrapy.Item):
    title = scrapy.Field()
    image = scrapy.Field()
    event_url = scrapy.Field()
    date_time = scrapy.Field()
    location = scrapy.Field()
    tags = scrapy.Field()
    all_text = scrapy.Field()
    
