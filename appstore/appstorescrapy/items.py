# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.item import Item, Field

class AppstorescrapyItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    date = Field()
    competitor_id = Field()
    appstore_id = Field()
    name = Field()
    downloads = Field(serializer=float)
    comments = Field(serializer=int)
    rate = Field(serializer=float)
    favs = Field(serializer=int)
    middles = Field(serializer=int)
    dislikes = Field(serializer=int)
    last_version = Field()
    last_comment = Field()

