# -*- coding: utf-8 -*-
import re
import json
import scrapy
import datetime

from scrapy import log
from scrapy.http import Request

from appstorescrapy.items import AppstorescrapyItem

class AppstorelenovoSpider(scrapy.Spider):
    name = "appstorelenovo"
    allowed_domains = ["lenovo.com"]
    start_urls = (
        'http://app.lenovo.com/app/15180324.html',   # 口袋故事听听
        'http://app.lenovo.com/app/15259140.html',   # 儿歌多多
        'http://app.lenovo.com/app/15224930.html',   # 宝贝听听
        'http://app.lenovo.com/app/15248582.html',   # 小伴龙
        'http://app.lenovo.com/app/15258923.html',   # 贝瓦儿歌
        'http://app.lenovo.com/app/15258977.html',   # 开心熊宝
        'http://app.lenovo.com/app/15053783.html',   # 快乐孕期
        'http://app.lenovo.com/app/15231732.html',   # 柚柚育儿
        'http://app.lenovo.com/app/15243197.html',   # 亲宝宝
    )

    def parse(self, response):
#        print response.body
        item = AppstorescrapyItem()

         # 获取爬虫运行时间
        now = datetime.datetime.now()
        item["date"] = now.strftime('%Y-%m-%d')

        # 获取竞品标识
        item['competitor_id'] = ""
        try:
            item['competitor_id'] = response.url.split("/")[-1].split(".")[0]
        except: pass

        # 获取应用市场标识
        item['appstore_id'] = self.name

        # 获取竞品名
        item['name'] = ''
        try:
            name_xpath = response.xpath("/html/body/div[@class='w1000 bcenter detailBox']/div[@class='fl wrapperLeft']/div[@class='leftBox border1 boxShadow fl']/div[@class='detailTop']/div[@class='detailTopL clearfix']/div[@class='detailMajor clearfix']/div[@class='fl']/div[@class='ff-wryh detailAppname txtCut']/h1[@class='f18 fl']/text()")
            name_text = name_xpath.extract()[0]
            item['name'] = name_text.strip()
        except Exception as e:
            log.msg("Error on analyzing name: " + str(e), log.WARNING)

        # 获取竞品下载次数
        item['downloads'] = 0
        try:
            download_xpath = response.xpath("/html/body/div[@class='w1000 bcenter detailBox']/div[@class='fl wrapperLeft']/div[@class='leftBox border1 boxShadow fl']/div[@class='detailTop']/div[@class='detailTopL clearfix']/div[@class='detailMajor clearfix']/div[@class='fl']/div[@class='f12 detailDownNum cb clearfix']/span[@class='fgrey5']/text()")
            download_text = download_xpath.extract()[0].strip()
            if download_text.endswith(u"万次安装"):
                download_text_pattern = re.compile(u"下载：(\d*)万次安装")
                downloads = re.findall(download_text_pattern, download_text)
                item['downloads'] = float(downloads[0])
            elif download_text.endswith(u"亿次安装"):
                download_text_pattern = re.compile(u"下载：(.+?)亿次安装")
                downloads = re.findall(download_text_pattern, download_text)
                item['downloads'] = float(downloads[0]) * 10000
        except Exception as e:
            log.msg("Error on analyzing downloads: " + str(e), log.WARNING)

        item['comments'] = 0

        item['rate'] = 0

        item['favs'] = 0

        item['middles'] = 0

        item['dislikes'] = 0

        item['last_version'] = ""
        try:
            version_xpath = response.xpath("/html/body/div[@class='w1000 bcenter detailBox']/div[@class='fl wrapperLeft']/div[@class='leftBox border1 boxShadow fl']/div[@class='detailTop']/div[@class='detailTopL clearfix']/div[@class='detailMajor clearfix']/div[@class='fl']/ul[@class='detailAppInfo fl']/li[@class='f12 fgrey4 txtCut'][2]/span[@class='fgrey5']/text()")
            version_text = version_xpath.extract()[0]
            item['last_version'] = version_text.strip()
        except Exception as e:
            log.msg("Error on analyzing last version: " + str(e), log.WARNING)

        item['last_comment'] = ""

        # http://apk.hiapk.com/web/api.do?qt=1701&id=2935565&pi=1&ps=10
        next_url = ""
        try:
            id_xpath = response.xpath("/html/body/div[@class='w1000 bcenter detailBox']/div[@class='fl wrapperLeft']/div[@class='leftBox border1 boxShadow fl']/div[@class='detailTop']/ul[@class='detailTop2 fgrey5']/li[@class='liFirst']/a[@class='icons btn-7 fl']")
            id_text = id_xpath.extract()[0]
            id_text = id_text.split()[2][14:-1]
            next_url = 'http://app.lenovo.com/getcommentlist.do?pn=%s&vc=128&si=1&c=10' % id_text
        except Exception as e:
            log.msg("Error on analyzing app id: " + str(e), log.WARNING)

        if next_url:
            yield Request(next_url, meta={'item': item, 'id': id_text}, callback=self.parse_comment)
        else:
            yield item

    def parse_comment(self, response):
        item = response.meta['item']
        id_text = response.meta['id']
        try:
            comments = json.loads(response.body)
            comment_details = comments['datalist']
            last_comment = ""
            for c in comment_details:
                last_comment = last_comment + c["content"] + "||"
            item['last_comment'] = last_comment
        except Exception as e:
            log.msg("Error on analyzing last comment: " + str(e), log.WARNING)

        # return next request
        next_url = "http://app.lenovo.com/getappscore.do?pn=%s&vc=128" % id_text
        yield Request(next_url, meta={'item': item, 'id': id_text}, callback=self.parse_rate)

    def parse_rate(self, response):
        item = response.meta['item']
        try:
            comments = json.loads(response.body)
            item['comments'] = comments['numberOfTotal']
            item['rate'] = comments['averageStar']
        except Exception as e:
            log.msg("Error on analyzing rate: " + str(e), log.WARNING)

        yield item
