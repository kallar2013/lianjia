# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy

class Xiaoqu(scrapy.Item):
    class_name = 'xq'
    
    mid = scrapy.Field()
    name = scrapy.Field()
    house_type_num = scrapy.Field()
    thirty_days = scrapy.Field()
    ninety_days = scrapy.Field()
    onrent = scrapy.Field()
    mtype = scrapy.Field()
    built_year = scrapy.Field()
    subway = scrapy.Field()
    school = scrapy.Field()
    price = scrapy.Field()
    onsale = scrapy.Field()
    plate = scrapy.Field()
    district = scrapy.Field()
    city = scrapy.Field()

class Chengjiao(scrapy.Item):
    class_name = 'cj'
    
    mid = scrapy.Field()
    xq_name = scrapy.Field()
    xq_id = scrapy.Field()
    house_type = scrapy.Field()
    size = scrapy.Field()
    storey = scrapy.Field()
    orientation = scrapy.Field()
    mtype = scrapy.Field()
    built_year = scrapy.Field()
    decoration = scrapy.Field()
    subway = scrapy.Field()
    school = scrapy.Field()
    five_year = scrapy.Field()
    two_year = scrapy.Field()
    elevator = scrapy.Field()
    deal_date = scrapy.Field()
    unit_price = scrapy.Field()
    total_price = scrapy.Field()

class Ershoufang(scrapy.Item):
    class_name = 'esf'
    
    mid = scrapy.Field()
    title = scrapy.Field()
    xq_id = scrapy.Field()
    house_type = scrapy.Field()
    size = scrapy.Field()
    orientation = scrapy.Field()
    decoration = scrapy.Field()
    elevator = scrapy.Field()
    storey = scrapy.Field()
    built_year = scrapy.Field()
    mtype = scrapy.Field()
    focus = scrapy.Field()
    visited = scrapy.Field()
    publish_date = scrapy.Field()
    five_year = scrapy.Field()
    two_year = scrapy.Field()
    school = scrapy.Field()
    subway = scrapy.Field()
    total_price = scrapy.Field()
    unit_price = scrapy.Field()
    crawl_date = scrapy.Field()
    
class Zufang(scrapy.Item):
    class_name = 'zf'
    
    mid = scrapy.Field()
    title = scrapy.Field()
    xq_id = scrapy.Field()
    house_type = scrapy.Field()
    size = scrapy.Field()
    orientation = scrapy.Field()
    storey = scrapy.Field()
    built_year = scrapy.Field()
    mtype = scrapy.Field()
    visited = scrapy.Field()
    last_updated = scrapy.Field()
    subway = scrapy.Field()
    heat = scrapy.Field()
    decoration = scrapy.Field()
    balcony = scrapy.Field()
    only = scrapy.Field()
    rent = scrapy.Field()
    other_tags = scrapy.Field()
    crawl_date = scrapy.Field()
    
class Plate(scrapy.Item):
    class_name = 'plate'
    
    name = scrapy.Field()
    url = scrapy.Field()
    
class Ershoufang_sh(scrapy.Item):
    class_name = 'esf'
    
    mid = scrapy.Field()
    xq_id = scrapy.Field()
    title = scrapy.Field()
    house_type = scrapy.Field()
    built_year = scrapy.Field()
    size = scrapy.Field()
    orientation = scrapy.Field()
    storey = scrapy.Field()
    visited = scrapy.Field()
    five_year = scrapy.Field()
    two_year = scrapy.Field()
    haskey = scrapy.Field()
    subway = scrapy.Field()
    total_price = scrapy.Field()
    unit_price = scrapy.Field()
    crawl_date = scrapy.Field()
    

class Xiaoqu_sh(scrapy.Item):
    class_name = 'xq'
    
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
    
class Chengjiao_sh(scrapy.Item):
    class_name = 'cj'
    
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