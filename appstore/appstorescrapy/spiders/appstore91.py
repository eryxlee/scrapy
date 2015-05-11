# -*- coding: utf-8 -*-
import re
import scrapy
import datetime

from scrapy import log

from appstorescrapy.items import AppstorescrapyItem


class Appstore91Spider(scrapy.Spider):
    name = "appstore91"
    allowed_domains = ["91.com"]
    start_urls = (
        'http://apk.91.com/Soft/Android/com.appshare.android.ilisten.html',   # 口袋故事听听
        'http://apk.91.com/Soft/Android/com.duoduo.child.story.html',         # 儿歌多多
        'http://apk.91.com/Soft/Android/com.xiaobanlong.main.html',           # 小伴龙
        'http://apk.91.com/Soft/Android/com.kunpeng.babyting.html',           # 宝贝听听
        'http://apk.91.com/Soft/Android/com.slanissue.apps.mobile.erge.html', # 贝瓦儿歌
        'http://apk.91.com/Soft/Android/com.iflytek.hipanda.html',            # 开心熊宝
        'http://apk.91.com/Soft/Android/com.babytree.apps.pregnancy.html',    # 快乐孕期
        'http://apk.91.com/Soft/Android/dianyun.baobaowd.html',               # 柚柚育儿
        'http://apk.91.com/Soft/Android/com.dw.btime.html',                   # 亲宝宝育儿
    )

    def parse(self, response):
        item = AppstorescrapyItem()

         # 获取爬虫运行时间
        now = datetime.datetime.now()
        item["date"] = now.strftime('%Y-%m-%d')

        # 获取竞品标识
        item['competitor_id'] = ""
        try:
            item['competitor_id'] = response.url.split("/")[-1].split('-')[0]
        except: pass

        # 获取应用市场标识
        item['appstore_id'] = self.name

        # 获取竞品名
        item['name'] = ''
        try:
            name_xpath = response.xpath("/html/body/div[@class='wrapper p_r clearfix']/div[@class='clearfix']/div[@class='w_693 fl']/div[@class='box s_intro clearfix']/div[@class='clearfix']/div[@class='s_intro_txt clearfix fr p_r']/div[@class='s_title clearfix']/h1[@class='ff f20 fb fl']/text()")
            name_text = name_xpath.extract()[0]
            item['name'] = name_text.strip()
        except Exception as e:
            log.msg("Error on analyzing name: " + str(e), log.WARNING)

        # 获取竞品下载次数
        item['downloads'] = 0
        try:
            download_xpath = response.xpath("/html/body/div[@class='wrapper p_r clearfix']/div[@class='clearfix']/div[@class='w_693 fl']/div[@class='box s_intro clearfix']/div[@class='clearfix']/div[@class='s_intro_txt clearfix fr p_r']/ul[@class='s_info']/li[2]/text()")
            download_text = download_xpath.extract()[0].strip()
            download_text_pattern = re.compile(u"下载次数：(\d*)万")
            downloads = re.findall(download_text_pattern, download_text)
            item['downloads'] = int(downloads[0])
        except Exception as e:
            log.msg("Error on analyzing downloads: " + str(e), log.WARNING)

        # 获取竞品评论次数，目前360.cn的评论数是通过JS获取的，目前取不到
        item['comments'] = 0
        # try:
        #     comment_xpath = response.xpath("/html/body[@class='index']/div[@class='warp']/div[@class='warper']/div[@class='main clearfix']/div[@class='main-left fl']/div[@id='app-info-panel']/div[@class='product btn_type1']/dl[@class='clearfix']/dd/div[@class='pf']/span[@class='s-2']/a[@id='comment-num']/text()")
        #     print  comment_xpath.extract()
        #     comment_text = comment_xpath.extract()[0]
        #     comment_text_pattern = re.compile(u"(\d*)条评价")
        #     comments = re.findall(comment_text_pattern, comment_text)
        #     item['comments'] = int(comments[0])
        # except Exception as e:
        #     log.msg("Error on analyzing comments: " + str(e), log.WARNING)

        item['rate'] = 0

        item['favs'] = 0
        try:
            fav_xpath = response.xpath("/html/body/div[@class='wrapper p_r clearfix']/div[@class='clearfix']/div[@class='w_693 fl']/div[@class='box s_intro clearfix']/div[@class='clearfix']/div[@class='s_intro_pic fl']/a[@class='ding spr']/text()")
            fav_text = fav_xpath.extract()[0].strip()
            if fav_text.endswith(u"万"):
                fav_text_pattern = re.compile(u"(\d*)万")
                favs = re.findall(fav_text_pattern, fav_text)
                item['favs'] = int(favs[0]) * 10000
            else:
                item['favs'] = int(fav_text)
        except Exception as e:
            log.msg("Error on analyzing favs: " + str(e), log.WARNING)

        item['middles'] = 0

        item['dislikes'] = 0
        try:
            dislike_xpath = response.xpath("/html/body/div[@class='wrapper p_r clearfix']/div[@class='clearfix']/div[@class='w_693 fl']/div[@class='box s_intro clearfix']/div[@class='clearfix']/div[@class='s_intro_pic fl']/a[@class='cai spr']/text()")
            dislike_text = dislike_xpath.extract()[0].strip()
            if dislike_text.endswith(u"万"):
                dislike_text_pattern = re.compile(u"(\d*)万")
                dislikes = re.findall(dislike_text_pattern, dislike_text)
                item['dislikes'] = int(dislikes[0]) * 10000
            else:
                item['dislikes'] = int(dislike_text)
        except Exception as e:
            log.msg("Error on analyzing dislikes: " + str(e), log.WARNING)

        item['last_version'] = ""
        try:
            version_xpath = response.xpath("/html/body/div[@class='wrapper p_r clearfix']/div[@class='clearfix']/div[@class='w_693 fl']/div[@class='box s_intro clearfix']/div[@class='clearfix']/div[@class='s_intro_txt clearfix fr p_r']/ul[@class='s_info']/li[1]/text()")
            version_text = version_xpath.extract()[0]
            item['last_version'] = version_text.strip()
        except Exception as e:
            log.msg("Error on analyzing last version: " + str(e), log.WARNING)

        item['last_comment'] = ""

        return item

