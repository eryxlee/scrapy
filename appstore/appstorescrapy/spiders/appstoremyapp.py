# -*- coding: utf-8 -*-
import re
import json
import scrapy
import datetime

from scrapy import log
from scrapy.http import Request

from appstorescrapy.items import AppstorescrapyItem

class AppstoremyappSpider(scrapy.Spider):
    name = "appstoremyapp"
    allowed_domains = ["myapp.com"]
    start_urls = (
        'http://android.myapp.com/myapp/detail.htm?apkName=com.appshare.android.ilisten',  #口袋故事听听
        'http://android.myapp.com/myapp/detail.htm?apkName=com.duoduo.child.story',  #儿歌多多
        'http://android.myapp.com/myapp/detail.htm?apkName=com.xiaobanlong.main',  #小伴龙
        'http://android.myapp.com/myapp/detail.htm?apkName=com.kunpeng.babyting',  #宝贝听听
        'http://android.myapp.com/myapp/detail.htm?apkName=com.slanissue.apps.mobile.erge',  #贝瓦儿歌
        'http://android.myapp.com/myapp/detail.htm?apkName=com.iflytek.hipanda',  #开心熊宝
        'http://android.myapp.com/myapp/detail.htm?apkName=com.babytree.apps.pregnancy',  #快乐孕期
        'http://android.myapp.com/myapp/detail.htm?apkName=dianyun.baobaowd',  #柚柚育儿
        'http://android.myapp.com/myapp/detail.htm?apkName=com.dw.btime',  #亲宝宝育儿
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
            name_xpath = response.xpath("/html/body/div[@id='J_DetDataContainer']/div[@class='det-main-container']/div[@class='det-ins-container J_Mod ']/div[@class='det-ins-data']/div[@class='det-name']/div[@class='det-name-int']/text()")
            name_text = name_xpath.extract()[0]
            item['name'] = name_text.strip()
        except Exception as e:
            log.msg("Error on analyzing name: " + str(e), log.WARNING)

        # 获取竞品下载次数
        item['downloads'] = 0
        try:
            download_xpath = response.xpath("/html/body/div[@id='J_DetDataContainer']/div[@class='det-main-container']/div[@class='det-ins-container J_Mod ']/div[@class='det-ins-data']/div[@class='det-insnum-line']/div[@class='det-ins-num']/text()")
            download_text = download_xpath.extract()[0].strip()
            if download_text.endswith(u"万下载"):
                download_text_pattern = re.compile(u"(\d*)万下载")
                downloads = re.findall(download_text_pattern, download_text)
                item['downloads'] = float(downloads[0])
            elif download_text.endswith(u"亿下载"):
                download_text_pattern = re.compile(u"(.+?)亿下载")
                downloads = re.findall(download_text_pattern, download_text)
                item['downloads'] = float(downloads[0]) * 10000
            else:
                download_text_pattern = re.compile(u"(\d*)下载")
                downloads = re.findall(download_text_pattern, download_text)
                item['downloads'] = float(downloads[0]) / 10000
        except Exception as e:
            log.msg("Error on analyzing downloads: " + str(e), log.WARNING)

        item['rate'] = 0
        try:
            rate_xpath = response.xpath("/html/body/div[@id='J_DetDataContainer']/div[@class='det-main-container']/div[@class='det-ins-container J_Mod ']/div[@class='det-ins-data']/div[@class='det-star-box']/div[@class='com-blue-star-num']/text()")
            rate_text = rate_xpath.extract()[0].strip()
            rate_text_pattern = re.compile(u"(.+?)分")
            rate = re.findall(rate_text_pattern, rate_text)
            item['rate'] = float(rate[0])
        except Exception as e:
            log.msg("Error on analyzing rate: " + str(e), log.WARNING)

        # 获取竞品评论次数
        item['comments'] = 0

        item['favs'] = 0

        item['middles'] = 0

        item['dislikes'] = 0

        item['last_version'] = ""
        try:
            version_xpath = response.xpath("/html/body/div[@id='J_DetDataContainer']/div[@class='det-main-container']/div[@class='det-othinfo-container J_Mod']/div[@class='det-othinfo-data'][1]/text()")
            version_text = version_xpath.extract()[0]
            item['last_version'] = version_text.strip()
        except Exception as e:
            log.msg("Error on analyzing last version: " + str(e), log.WARNING)

        item['last_comment'] = ""

        # return next request
        next_url = "http://android.myapp.com/myapp/app/comment.htm?apkName=" + item['competitor_id']
        yield Request(next_url, meta={'item': item}, callback=self.parse_comment)

    def parse_comment(self, response):
        item = response.meta['item']
        try:
            comments = json.loads(response.body)
            item['comments'] = comments['obj']['total']
            comment_details = comments['obj']['commentDetails']
            last_comment = ""
            for c in comment_details:
                last_comment = last_comment + c["content"] + "||"
            item['last_comment'] = last_comment
        except Exception as e:
            log.msg("Error on analyzing last comment: " + str(e), log.WARNING)

        yield item
