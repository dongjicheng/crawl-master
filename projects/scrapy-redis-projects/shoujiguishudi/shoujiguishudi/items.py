# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class PhoneNumItem(Item):
    _seed = Field()
    phonenumber = Field()
    province = Field()
    city = Field()
    company = Field()


class FailedItem(Item):
    _seed = Field()