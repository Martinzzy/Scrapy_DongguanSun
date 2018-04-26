# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,MapCompose


class ScrapyDongguansunItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def get_id(value):
    res = re.search('.*?(\d+)',value)
    return int(res.group(1))

def get_title(value):
    res = value.split()[0].replace('提问：','')
    return res

def get_content(value):
    res = ''.join(value.split())
    return res

class DongguanSunItemLoader(ItemLoader):

    default_output_processor = TakeFirst()

class DongguanSunItem(scrapy.Item):

    url = scrapy.Field()
    title = scrapy.Field(input_processor = MapCompose(get_title))
    id = scrapy.Field(input_processor = MapCompose(get_id))
    content = scrapy.Field(input_processor = MapCompose(get_content))
    status = scrapy.Field()
    crawl_time = scrapy.Field()