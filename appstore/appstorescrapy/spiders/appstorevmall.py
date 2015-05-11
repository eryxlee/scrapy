# -*- coding: utf-8 -*-
import re
import json
import scrapy
import datetime

from scrapy import log
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from appstorescrapy.items import AppstorescrapyItem

class AppstorevmallSpider(scrapy.Spider):
    name = "appstorevmall"
    allowed_domains = ["vmall.com"]
    start_urls = (
        'http://app.vmall.com/app/C55044',       #口袋故事听听
        'http://app.vmall.com/app/C10087276',    #儿歌多多
        'http://app.vmall.com/app/C34509',       #宝贝听听
        'http://app.vmall.com/app/SC67132',      #小伴龙
        'http://app.vmall.com/app/C10083662',    #贝瓦儿歌
        'http://app.vmall.com/app/SC57048',      #开心熊宝
        'http://app.vmall.com/app/C43237',       #快乐孕期
        'http://app.vmall.com/app/C10061154',    #柚柚育儿
        'http://app.vmall.com/app/C191426',      #亲宝宝育儿
    )

    def parse(self, response):
        item = AppstorescrapyItem()

         # 获取爬虫运行时间
        now = datetime.datetime.now()
        item["date"] = now.strftime('%Y-%m-%d')

        # 获取竞品标识
        item['competitor_id'] = ""
        try:
            item['competitor_id'] = response.url.split("/")[-1]
        except: pass

        # 获取应用市场标识
        item['appstore_id'] = self.name

        # 获取竞品名
        item['name'] = ''
        try:
            name_xpath = response.xpath("/html/body[@id='bodyonline']/div[@class='lay-body']/div[@class='lay-main']/div[@class='lay-left hdn-x']/div[@class='unit nofloat prsnRe']/div[@class='unit-main detail-part']/div[@class='app-info flt']/ul[@class='app-info-ul nofloat'][1]/li[2]/p[1]/span[@class='title']/text()")
            name_text = name_xpath.extract()[0]
            item['name'] = name_text.strip()
        except Exception as e:
            log.msg("Error on analyzing name: " + str(e), log.WARNING)

        # 获取竞品下载次数
        item['downloads'] = 0
        try:
            download_xpath = response.xpath("/html/body[@id='bodyonline']/div[@class='lay-body']/div[@class='lay-main']/div[@class='lay-left hdn-x']/div[@class='unit nofloat prsnRe']/div[@class='unit-main detail-part']/div[@class='app-info flt']/ul[@class='app-info-ul nofloat'][1]/li[2]/p[1]/span[@class='grey sub']/text()")
            download_text = download_xpath.extract()[0].strip()
            download_text_pattern = re.compile(u"下载：(\d*)次")
            downloads = re.findall(download_text_pattern, download_text)
            item['downloads'] = int(downloads[0]) * 1.0 / 10000
        except Exception as e:
            log.msg("Error on analyzing downloads: " + str(e), log.WARNING)

        item['comments'] = 0

        item['rate'] = 0

        item['favs'] = 0

        item['middles'] = 0

        item['dislikes'] = 0

        item['last_version'] = ""
        try:
            version_xpath = response.xpath("/html/body[@id='bodyonline']/div[@class='lay-body']/div[@class='lay-main']/div[@class='lay-left hdn-x']/div[@class='unit nofloat prsnRe']/div[@class='unit-main detail-part']/div[@class='app-info flt']/ul[@class='app-info-ul nofloat'][2]/li[@class='ul-li-detail'][4]/span/text()")
            version_text = version_xpath.extract()[0]
            item['last_version'] = version_text.strip()
        except Exception as e:
            log.msg("Error on analyzing last version: " + str(e), log.WARNING)

        item['last_comment'] = ""

        # return next request
        next_url = "http://app.vmall.com/comment/commentAction.action?appId=" + item['competitor_id']
        yield Request(next_url, meta={'item': item}, callback=self.parse_comment)

    def parse_comment(self, response):
        item = response.meta['item']
        try:
            comment_xpath = response.xpath("/html/body/form[@id='commentForm']/h4[@class='sub nofloat']/span[@class='title']/text()")
            comment_text = comment_xpath.extract()[0].strip()
            pos1 = comment_text.find(u'（')
            pos2 = comment_text.find(u'条')
            comments = comment_text[pos1 + 1: pos2]
            item['comments'] = int(comments)
        except Exception as e:
            log.msg("Error on analyzing comments: " + str(e), log.WARNING)

        try:
            hxs = HtmlXPathSelector(response)
            comment_selectors = hxs.select('//div[@class="comment"]')

            last_comment = ""
            for s in comment_selectors:
                last_comment = last_comment + s.select('p/text()').extract()[0].strip() + "||"
            item['last_comment'] = last_comment
        except Exception as e:
            log.msg("Error on analyzing last comments: " + str(e), log.WARNING)

        yield item

