# -*- coding: utf-8 -*-

# Scrapy settings for sexy project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'sexy'

SPIDER_MODULES = ['sexy.spiders']
NEWSPIDER_MODULE = 'sexy.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'sexy (+http://www.yourdomain.com)'

FILES_STORE = "/Volumes/archive/backups/a"

ITEM_PIPELINES = {'sexy.pipelines.MyImagesPipeline': 1}

