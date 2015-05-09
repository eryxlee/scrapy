# -*- coding: utf-8 -*-
import scrapy
import shutil

from scrapy import log
from scrapy.http import Request

from sexy.items import SexyItem

class SexyfaceksSpider(scrapy.Spider):
    name = "sexyfaceks"
    allowed_domains = ["sexy.faceks.com"]
    start_urls = (
        'http://sexy.faceks.com',
    )

    def parse(self, response):
        log.msg("Find a page: " + response.url)

        try:
            post_list = response.xpath("//div[@class='ct']/div[@class='ctc box']")
            for post in post_list:
                item = SexyItem()
                # get the name of this post
                name = post.xpath("div[@class='text']/p/text()").extract()[0].strip()
                normal_name = u' '.join(name.split())
                item['name'] = normal_name
                item['dirname'] = normal_name

                # if name is too long, discard
                if len(normal_name) > 32: continue
                # get the url of this post
                post_url = post.xpath("div[@class='pic']/a[@class='img']/@href").extract()[0].strip()
                log.msg("@@@@Find model %s with post url %s." % (normal_name, post_url))
                if post_url:
                    yield Request(post_url, meta={'item': item}, callback=self.parse_deltail)

        except Exception as e:
            log.msg("Error on analyzing post list: " + str(e), log.WARNING)

        try:
            nextpage = response.xpath("//div[@id='m-pager-idx']/a[@class='next']/@href")
            next_url = self.start_urls[0] + "/" + nextpage.extract()[0]
            yield Request(next_url)
        except Exception as e:
            log.msg("Error on analyzing pager index: " + str(e), log.WARNING)

    def parse_deltail(self, response):
        item = response.meta['item']
        try:
            img_list = response.xpath("//div[@class='ctc box']/div[@class='pic']/a[@class='img imgclasstag']/@bigimgsrc").extract()
            log.msg("@@@Find %d photos of %s." % (len(img_list), item['name']))
            item["file_urls"] = img_list

            date = response.xpath("//div[@class='lnks box']/a[@class='date']/text()").extract()[0].strip()
            item['dirname'] = "%s(%s)" % (item['dirname'], date)
            return item
        except Exception as e:
            log.msg("Error on analyzing detail: " + str(e), log.WARNING)

