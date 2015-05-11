# -*- coding: utf-8 -*-
import re
import json
import scrapy
import datetime

from scrapy import log
from scrapy.http import Request

from appstorescrapy.items import AppstorescrapyItem


class Appstore360Spider(scrapy.Spider):
    name = "appstore360"
    allowed_domains = ["360.cn"]
    start_urls = (
        'http://zhushou.360.cn/detail/index/soft_id/125213',  # 口袋故事听听
        'http://zhushou.360.cn/detail/index/soft_id/841182',   # 儿歌多多
        'http://zhushou.360.cn/detail/index/soft_id/155167',  # 小伴龙
        'http://zhushou.360.cn/detail/index/soft_id/72852',   # 宝贝听听
        'http://zhushou.360.cn/detail/index/soft_id/525578',  # 贝瓦儿歌
        'http://zhushou.360.cn/detail/index/soft_id/118651',  # 开心熊宝
        'http://zhushou.360.cn/detail/index/soft_id/98095',   # 快乐孕期
        'http://zhushou.360.cn/detail/index/soft_id/708727',  # 柚柚育儿
        'http://zhushou.360.cn/detail/index/soft_id/198622',  # 亲宝宝-育儿怀孕
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
            name_xpath = response.xpath("/html/body[@class='index']/div[@class='warp']/div[@class='warper']/div[@class='main clearfix']/div[@class='main-left fl']/div[@id='app-info-panel']/div[@class='product btn_type1']/dl[@class='clearfix']/dd/h2[@id='app-name']/span/text()")
            name_text = name_xpath.extract()[0]
            item['name'] = name_text.strip()
        except Exception as e:
            log.msg("Error on analyzing name: " + str(e), log.WARNING)

        # 获取竞品下载次数
        item['downloads'] = 0
        try:
            download_xpath = response.xpath("/html/body[@class='index']/div[@class='warp']/div[@class='warper']/div[@class='main clearfix']/div[@class='main-left fl']/div[@id='app-info-panel']/div[@class='product btn_type1']/dl[@class='clearfix']/dd/div[@class='pf']/span[@class='s-3'][1]/text()")
            download_text = download_xpath.extract()[0].strip()
            download_text_pattern = re.compile(u"下载：(\d*)万次")
            downloads = re.findall(download_text_pattern, download_text)
            item['downloads'] = int(downloads[0])
        except Exception as e:
            log.msg("Error on analyzing downloads: " + str(e), log.WARNING)

        item['comments'] = 0

        item['rate'] = 0

        item['favs'] = 0

        item['middles'] = 0

        item['dislikes'] = 0

        item['last_version'] = ""
        try:
            version_xpath = response.xpath("/html/body[@class='index']/div[@class='warp']/div[@class='warper']/div[@class='main clearfix']/div[@class='main-left fl']/div[@class='infors']/div[@class='mod-info']/div[@class='infors-txt']/div[@id='sdesc']/div[@class='breif']/div[@class='base-info']/table/tbody/tr[2]/td[1]/text()")
            version_text = version_xpath.extract()[0]
            item['last_version'] = version_text.strip()
        except Exception as e:
            log.msg("Error on analyzing last version: " + str(e), log.WARNING)

        item['last_comment'] = ""

        ids_xpath = response.xpath("//script")
        ids_text = ids_xpath.extract()[7]
        ids_text = ids_text.split('\n')[13]
        ids_text = ids_text.split('\'')[3]

        # return next request
        next_url = "http://intf.baike.360.cn/index.php?name=%s&c=poll&a=getpoll" % ids_text
        yield Request(next_url,
            meta={'item': item, 'id': ids_text, 'refer': response.url},
            headers={'Referer': response.url},
            callback=self.parse_rate)

    def parse_rate(self, response):
        item = response.meta['item']
        ids_text = response.meta['id']
        refer = response.meta['refer']
        try:
            rate = json.loads(response.body)
            item['rate'] = rate['data']['cscore']
        except Exception as e:
            log.msg("Error on analyzing rate: " + str(e), log.WARNING)

        next_url = "http://intf.baike.360.cn/index.php?name=%s&c=message&a=getmessagenum" % ids_text
        yield Request(next_url,
            meta={'item': item, 'id': ids_text, 'refer': refer},
            headers={'Referer': refer},
            callback=self.parse_comment_count)

    def parse_comment_count(self, response):
        item = response.meta['item']
        ids_text = response.meta['id']
        refer = response.meta['refer']
        try:
            comment_count = json.loads(response.body)
            item['comments'] = comment_count['mesg']
            item['favs'] = comment_count['best']
            item['middles'] = comment_count['good']
            item['dislikes'] = comment_count['bad']
        except Exception as e:
            log.msg("Error on analyzing comments: " + str(e), log.WARNING)

        next_url = "http://intf.baike.360.cn/index.php?name=%s&c=message&a=getmessage&start=10&count=10" % ids_text
        yield Request(next_url,
            meta={'item': item, 'id': ids_text, 'refer': refer},
            headers={'Referer': refer},
            callback=self.parse_comment)

    def parse_comment(self, response):
        item = response.meta['item']
        ids_text = response.meta['id']
        try:
            comments = json.loads(response.body)
            comment_details = comments['data']['messages']
            last_comment = ""
            for c in comment_details:
                last_comment = last_comment + c["content"] + "||"
            item['last_comment'] = last_comment
        except Exception as e:
            log.msg("Error on analyzing last comment: " + str(e), log.WARNING)

        yield item
