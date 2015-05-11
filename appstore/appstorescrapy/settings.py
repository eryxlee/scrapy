# -*- coding: utf-8 -*-

# Scrapy settings for appstorescrapy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'qibot'

SPIDER_MODULES = ['appstorescrapy.spiders']
NEWSPIDER_MODULE = 'appstorescrapy.spiders'

ITEM_PIPELINES = {
    'appstorescrapy.pipelines.CoercePipeline': 300,
    'appstorescrapy.pipelines.SaveDBPipeline': 800,
}

#LOG_LEVEL = "WARNING"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'appstorescrapy (+http://www.yourdomain.com)'
