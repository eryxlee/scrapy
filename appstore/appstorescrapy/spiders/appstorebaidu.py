# -*- coding: utf-8 -*-
import re
import json
import scrapy
import datetime

from scrapy import log
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector

from appstorescrapy.items import AppstorescrapyItem

class AppstorebaiduSpider(scrapy.Spider):
    name = "appstorebaidu"
    allowed_domains = ["baidu.com"]
    start_urls = (
        'http://shouji.baidu.com/soft/item?docid=6722489',        # 口袋故事听听
        'http://shouji.baidu.com/software/item?docid=6828600',    # 儿歌多多
        'http://shouji.baidu.com/soft/item?docid=6822756',        # 小伴龙
        'http://shouji.baidu.com/soft/item?docid=6789888',        # 宝贝听听
        'http://shouji.baidu.com/software/item?docid=6827852',    # 贝瓦儿歌
        'http://shouji.baidu.com/software/item?docid=6828397',    # 开心熊宝
        'http://shouji.baidu.com/soft/item?docid=6654357',        # 快乐孕期
        'http://shouji.baidu.com/soft/item?docid=6793181',        # 柚柚育儿
        'http://shouji.baidu.com/software/item?docid=6809263',    # 亲宝宝-育儿怀孕
    )

    def parse(self, response):
        item = AppstorescrapyItem()

         # 获取爬虫运行时间
        now = datetime.datetime.now()
        item["date"] = now.strftime('%Y-%m-%d')

        # 获取竞品标识
        item['competitor_id'] = ""
        try:
            item['competitor_id'] = response.url.split("=")[-1]
        except: pass

        # 获取应用市场标识
        item['appstore_id'] = self.name

        # 获取竞品名
        item['name'] = ''
        try:
            name_xpath = response.xpath("/html/body/div[@id='doc']/div[@class='yui3-g']/div[@class='yui3-u content-main']/div[@class='app-intro']/div[@class='intro-top']/div[@class='content-right']/h1[@class='app-name']/span/text()")
            name_text = name_xpath.extract()[0]
            item['name'] = name_text.strip()
        except Exception as e:
            log.msg("Error on analyzing name: " + str(e), log.WARNING)

        # 获取竞品下载次数
        item['downloads'] = 0
        try:
            download_xpath = response.xpath("/html/body/div[@id='doc']/div[@class='yui3-g']/div[@class='yui3-u content-main']/div[@class='app-intro']/div[@class='intro-top']/div[@class='content-right']/div[@class='detail']/span[@class='download-num']/text()")
            download_text = download_xpath.extract()[0].strip()
            if download_text.endswith(u"万"):
                download_text_pattern = re.compile(u"下载次数: (\d*)万")
                downloads = re.findall(download_text_pattern, download_text)
                item['downloads'] = float(downloads[0])
            elif download_text.endswith(u"亿"):
                download_text_pattern = re.compile(u"下载次数: (.+?)亿")
                downloads = re.findall(download_text_pattern, download_text)
                item['downloads'] = float(downloads[0]) * 10000
            else:
                item['downloads'] = float(download_text) / 10000
        except Exception as e:
            log.msg("Error on analyzing downloads: " + str(e), log.WARNING)

        item['rate'] = 0

        # 获取竞品评论次数
        item['comments'] = 0

        # 赞数量
        item['favs'] = 0

        item['middles'] = 0

        # 踩数量
        item['dislikes'] = 0

        # 版本信息
        item['last_version'] = ""
        try:
            version_xpath = response.xpath("/html/body/div[@id='doc']/div[@class='yui3-g']/div[@class='yui3-u content-main']/div[@class='app-intro']/div[@class='intro-top']/div[@class='content-right']/div[@class='detail']/span[@class='version']/text()")
            version_text = version_xpath.extract()[0]
            item['last_version'] = version_text.strip()
        except Exception as e:
            log.msg("Error on analyzing last version: " + str(e), log.WARNING)

        item['last_comment'] = ""

        # http://shouji.baidu.com/comment?action_type=getCommentList&groupid=2527769
        next_url = ""
        try:
            id_xpath = response.xpath("/html/body/div[@id='doc']/div[@class='yui3-g']/div[@class='yui3-u content-main']/div[@class='app-intro']//input[@type='hidden' and @name='groupid']/@value")
            id_text = id_xpath.extract()[0]
            next_url = 'http://shouji.baidu.com/comment?action_type=getCommentList&groupid=%s' % id_text
        except Exception as e:
            log.msg("Error on analyzing app id: " + str(e), log.WARNING)

        if next_url:
            yield Request(next_url, meta={'item': item}, callback=self.parse_comment)
        else:
            yield item

    def parse_comment(self, response):
        item = response.meta['item']
        try:
            hxs = HtmlXPathSelector(response)
            comment_selectors = hxs.select("//ol[@class='comment-list']/li[@class='comment']")

            last_comment = ""
            for s in comment_selectors:
                last_comment = last_comment + s.select("div[@class='comment-info']/div[2]/p/text()").extract()[0].strip() + "||"
            item['last_comment'] = last_comment
        except Exception as e:
            log.msg("Error on analyzing last comments: " + str(e), log.WARNING)

        yield item
