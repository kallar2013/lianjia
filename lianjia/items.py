# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Plate(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()

class Xiaoqu(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    mid = scrapy.Field()
    title = scrapy.Field()
    year = scrapy.Field()
    ditie = scrapy.Field()
    price = scrapy.Field()
    onsale = scrapy.Field()
    platename = scrapy.Field()
    district = scrapy.Field()
    city = scrapy.Field()
    coordinate = scrapy.Field()
    
class Chengjiao(scrapy.Item):
    mid = scrapy.Field()
    xq_name = scrapy.Field()
    size = scrapy.Field()
    house_type = scrapy.Field()
    storey = scrapy.Field()
    orientation = scrapy.Field()
    decoration = scrapy.Field()
    subway = scrapy.Field()
    five_year = scrapy.Field()
    two_year = scrapy.Field()
    deal_date = scrapy.Field()
    unit_price = scrapy.Field()
    total_price = scrapy.Field()