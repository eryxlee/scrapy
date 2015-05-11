# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os
import sys
import time
import errno
import socket
import select
import MySQLdb
import MySQLdb.cursors

from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request
from scrapy.exceptions import DropItem

class BasePipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',
            host='localhost',
            db = 'boss',
            user = 'root',
            passwd = '',
            cursorclass = MySQLdb.cursors.DictCursor,
            charset = 'utf8',
            use_unicode = True,
            cp_reconnect=True
        )

    def handle_error(self, e):
        log.err(e)

class SaveDBPipeline(BasePipeline):
    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self._conditional_insert, item)
        query.addErrback(self.handle_error)
        return item

    #将每行写入数据库中
    def _conditional_insert(self, tx, item):
        tx.execute("insert into aps_bss_crawl_log(date, appstore_id, competitor_id, name, downloads, comments, rate, favs, middles, dislikes, last_version, last_comment) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (item['date'], item['appstore_id'], item['competitor_id'], item['name'], item['downloads'], item['comments'], item['rate'],
                item['favs'], item['middles'], item['dislikes'], item['last_version'], item['last_comment']))


class CoercePipeline(BasePipeline):
    def __init__(self):
        BasePipeline.__init__(self)
        # 将竞品信息读取到缓存中
        self.appstore = []
        self.competitor = []
        query = self.dbpool.runInteraction(self.cache_competitor_info, self.appstore, self.competitor)
        query.addErrback(self.handle_error)

    def process_item(self, item, spider):
        # for rec in self.appstore:
        #     if rec["name"] == item["appstore_id"]:
        #         item["appstore_id"] = rec["id"]
        #         break
        for rec in self.competitor:
            if (rec["competitor_mark"] == item["competitor_id"] and rec["spider_name"] == item["appstore_id"]):
                item["competitor_id"] = rec["competitor_id"]
                item["appstore_id"] = rec["appstore_id"]
                break
        return item

    def cache_competitor_info(self, tx, appstore, competitor):
        # tx.execute("select * from aps_bss_appstore")
        # result = tx.fetchall()
        # if result:
        #     appstore.extend(result)
        tx.execute("SELECT A.id AS appstore_id, A.spider_name as spider_name, B.id as competitor_id, C.competitor_mark FROM boss.aps_bss_appstore A, boss.aps_bss_competitor_info B, boss.aps_bss_competitor_appstore C where A.id = C.appstore_id and B.id = C.competitor_id and A.status = 1 and B.status = 1")
        result = tx.fetchall()
        if result:
            competitor.extend(result)

