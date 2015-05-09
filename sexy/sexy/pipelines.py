# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# pip install pillow
import os

from scrapy.http import Request
from scrapy.contrib.pipeline.files import FilesPipeline

class MyImagesPipeline(FilesPipeline):

    def file_path(self, request, response=None, info=None):
        item=request.meta['item'] # Like this you can use all from item, not just url.
        image_guid = request.url.split('/')[-1]
        return '%s/%s' % (item["dirname"], image_guid)

    def get_media_requests(self, item, info):
        #yield Request(item['images']) # Adding meta. Dunno how to put it in one line :-)
        for image in item['file_urls']:
            yield Request(image, meta={'item': item})





