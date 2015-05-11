# -*- coding: utf-8 -*-
import re
import json
import scrapy
import datetime

from scrapy import log
from scrapy.http import Request

from appstorescrapy.items import AppstorescrapyItem

class AppstorewandoujiaSpider(scrapy.Spider):
    name = "appstorewandoujia"
    allowed_domains = ["wandoujia.com"]
    start_urls = (
        'http://www.wandoujia.com/apps/com.appshare.android.ilisten',  #口袋故事听听
        'http://www.wandoujia.com/apps/com.duoduo.child.story',        #儿歌多多
        'http://www.wandoujia.com/apps/com.xiaobanlong.main',          #小伴龙
        'http://www.wandoujia.com/apps/com.kunpeng.babyting',          #宝贝听听
        'http://www.wandoujia.com/apps/com.slanissue.apps.mobile.erge',#贝瓦儿歌
        'http://www.wandoujia.com/apps/com.iflytek.hipanda',           #开心熊宝
        'http://www.wandoujia.com/apps/com.babytree.apps.pregnancy',   #快乐孕期
        'http://www.wandoujia.com/apps/dianyun.baobaowd',              #柚柚育儿
        'http://www.wandoujia.com/apps/com.dw.btime',                  #亲宝宝育儿
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
            name_xpath = response.xpath("/html/body[@class='detail PC ']/div[@class='container']/div[@class='detail-wrap ']/div[@class='detail-top clearfix']/div[@class='app-info']/p[@class='app-name']/span[@class='title']/text()")
            name_text = name_xpath.extract()[0]
            item['name'] = name_text.strip()
        except Exception as e:
            log.msg("Error on analyzing name: " + str(e), log.WARNING)

        # 获取竞品下载次数
        item['downloads'] = 0
        try:
            download_xpath = response.xpath("/html/body[@class='detail PC ']/div[@class='container']/div[@class='detail-wrap ']/div[@class='detail-top clearfix']/div[@class='num-list']/span[@class='item']/i/text()")
            download_text = download_xpath.extract()[0].strip()
            if download_text.endswith(u"万"):
                download_text_pattern = re.compile(u"(\d*) 万")
                downloads = re.findall(download_text_pattern, download_text)
                item['downloads'] = float(downloads[0])
            elif download_text.endswith(u"亿"):
                download_text_pattern = re.compile(u"(.+?) 亿")
                downloads = re.findall(download_text_pattern, download_text)
                item['downloads'] = float(downloads[0]) * 10000
            else:
                item['downloads'] = float(download_text) / 10000
        except Exception as e:
            log.msg("Error on analyzing downloads: " + str(e), log.WARNING)

        # 获取竞品评论次数
        item['comments'] = 0
        try:
            comment_xpath = response.xpath("/html/body[@class='detail PC ']/div[@class='container']/div[@class='detail-wrap ']/div[@class='detail-top clearfix']/div[@class='num-list']/a[@class='item last comment-open']/i/text()")
            comment_text = comment_xpath.extract()[0].strip()
            item['comments'] = int(comment_text)
        except Exception as e:
            log.msg("Error on analyzing comments: " + str(e), log.WARNING)

        item['rate'] = 0

        item['favs'] = 0
        try:
            fav_xpath = response.xpath("/html/body[@class='detail PC ']/div[@class='container']/div[@class='detail-wrap ']/div[@class='detail-top clearfix']/div[@class='num-list']/span[@class='item love']/i/text()")
            fav_text = fav_xpath.extract()[0].strip()
            item['favs'] = int(fav_text)
        except Exception as e:
            log.msg("Error on analyzing favs: " + str(e), log.WARNING)

        item['middles'] = 0

        item['dislikes'] = 0

        item['last_version'] = ""
        try:
            version_xpath = response.xpath("/html/body[@class='detail PC ']/div[@class='container']/div[@class='detail-wrap ']/div[@class='cols clearfix'][1]/div[@class='col-right']/div[@class='infos']/dl[@class='infos-list']/dd[4]/text()")
            version_text = version_xpath.extract()[0]
            item['last_version'] = version_text.strip()
        except Exception as e:
            log.msg("Error on analyzing last version: " + str(e), log.WARNING)

        item['last_comment'] = ""

        # return next request
        next_url = "http://apps.wandoujia.com/api/v1/comments/primary?packageName=" + item['competitor_id']
        yield Request(next_url, meta={'item': item}, callback=self.parse_comment)

    def parse_comment(self, response):
        item = response.meta['item']
        try:
            comments = json.loads(response.body)
            comment_details = comments['comments']
            last_comment = ""
            for c in comment_details:
                last_comment = last_comment + c["content"] + "||"
            item['last_comment'] = last_comment
        except Exception as e:
            log.msg("Error on analyzing last comment: " + str(e), log.WARNING)

        yield item

