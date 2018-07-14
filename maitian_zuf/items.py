# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MaitianZufItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    zf_url = scrapy.Field()
    title = scrapy.Field()
    rent = scrapy.Field()
    floorage = scrapy.Field()
    orientation = scrapy.Field()
    decoration = scrapy.Field()
    area = scrapy.Field()
    way = scrapy.Field()
    comment = scrapy.Field()
    house_type = scrapy.Field()
    payment = scrapy.Field()
    feature = scrapy.Field()
    business = scrapy.Field()


class MaitianEsItem(scrapy.Item):
    es_url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    unit_pri = scrapy.Field()
    down_payment = scrapy.Field()
    floorage = scrapy.Field()
    orientation = scrapy.Field()
    area = scrapy.Field()
    comment = scrapy.Field()
    monthly_pay = scrapy.Field()
    house_type = scrapy.Field()
    floor = scrapy.Field()
    business = scrapy.Field()


