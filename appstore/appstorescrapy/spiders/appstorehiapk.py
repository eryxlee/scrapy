# -*- coding: utf-8 -*-
import re
import json
import scrapy
import datetime

from scrapy import log
from scrapy.http import Request

from appstorescrapy.items import AppstorescrapyItem

class AppstorehiapkSpider(scrapy.Spider):
    name = "appstorehiapk"
    allowed_domains = ["hiapk.com"]
    start_urls = (
        'http://apk.hiapk.com/appinfo/com.appshare.android.ilisten',   #口袋故事听听
        'http://apk.hiapk.com/appinfo/com.duoduo.child.story',         #儿歌多多
        'http://apk.hiapk.com/appinfo/com.xiaobanlong.main',           #小伴龙
        'http://apk.hiapk.com/appinfo/com.kunpeng.babyting',           #宝贝听听
        'http://apk.hiapk.com/appinfo/com.slanissue.apps.mobile.erge', #贝瓦儿歌
        'http://apk.hiapk.com/appinfo/com.iflytek.hipanda',            #开心熊宝
        'http://apk.hiapk.com/appinfo/com.babytree.apps.pregnancy',    #快乐孕期
        'http://apk.hiapk.com/appinfo/dianyun.baobaowd',               #柚柚育儿
        'http://apk.hiapk.com/appinfo/com.dw.btime',                   #亲宝宝育儿
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
            name_xpath = response.xpath("/html/body/div[@id='webInnerContent']/div/div[@class='detail_left']/div[@class='detail_content']/div[@class='left detail_description']/div[@id='appSoftName']/text()")
            name_text = name_xpath.extract()[0]
            item['name'] = name_text.strip()
        except Exception as e:
            log.msg("Error on analyzing name: " + str(e), log.WARNING)

        # 获取竞品下载次数
        item['downloads'] = 0
        try:
            download_xpath = response.xpath("/html/body/div[@id='webInnerContent']/div/div[@class='detail_right']/div[@class='code_box_border']/div[@class='line_content'][2]/span[@class='font14'][2]/text()")
            download_text = download_xpath.extract()[0].strip()
            download_text_pattern = re.compile(u"(.+?)热度")
            downloads = re.findall(download_text_pattern, download_text)
            if downloads[0].endswith(u"百万"):
                item['downloads'] = float(downloads[0][:len(downloads[0])-2]) * 100
            elif  downloads[0].endswith(u"千万"):
                item['downloads'] = float(downloads[0][:len(downloads[0])-2]) * 1000
            elif  downloads[0].endswith(u"亿"):
                item['downloads'] = float(downloads[0][:len(downloads[0])-1]) * 10000
            else:
                item['downloads'] = float(downloads[0][:len(downloads[0])-1])
        except Exception as e:
            log.msg("Error on analyzing downloads: " + str(e), log.WARNING)

        item['rate'] = 0
        try:
            rate_xpath = response.xpath("/html/body/div[@id='webInnerContent']/div/div[@class='detail_left']/div[@class='detail_content']/div[8]/div[@class='star_dotted']/div[@class='star_tip_div left']/div[@class='star_num']/text()")
            rate_text = rate_xpath.extract()[0].strip()
            item['rate'] = float(rate_text)
        except Exception as e:
            log.msg("Error on analyzing rate: " + str(e), log.WARNING)

        # 获取竞品评论次数
        item['comments'] = 0

        item['favs'] = 0

        item['middles'] = 0

        item['dislikes'] = 0

        item['last_version'] = ""
        try:
            version_xpath = response.xpath("/html/body/div[@id='webInnerContent']/div/div[@class='detail_left']/div[@class='detail_content']/div[@class='left detail_description']/div[@id='appSoftName']/text()")
            version_text = version_xpath.extract()[0]
            item['last_version'] = version_text.strip()
        except Exception as e:
            log.msg("Error on analyzing last version: " + str(e), log.WARNING)

        item['last_comment'] = ""

        # http://apk.hiapk.com/web/api.do?qt=1701&id=2935565&pi=1&ps=10
        next_url = ""
        try:
            id_xpath = response.xpath("/html/body/div[@id='webInnerContent']/div/div[@class='detail_left']//input[@type='hidden' and @id='hidAppId']/@value")
            id_text = id_xpath.extract()[0]
            next_url = 'http://apk.hiapk.com/web/api.do?qt=1701&id=%s&pi=1&ps=10' % id_text
        except Exception as e:
            log.msg("Error on analyzing app id: " + str(e), log.WARNING)

        if next_url:
            yield Request(next_url, meta={'item': item}, callback=self.parse_comment)
        else:
            yield item

    def parse_comment(self, response):
        item = response.meta['item']
        try:
            comments = json.loads(response.body)
            item['comments'] = comments['total']
            comment_details = comments['data']
            last_comment = ""
            for c in comment_details:
                last_comment = last_comment + c["content"] + "||"
            item['last_comment'] = last_comment
        except Exception as e:
            log.msg("Error on analyzing last comment: " + str(e), log.WARNING)

        yield item

