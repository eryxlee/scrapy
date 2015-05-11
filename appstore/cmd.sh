#!/bin/bash

SCRAPY="/Users/eryxlee/Workshops/python/sandbox/bin/scrapy"
PROJECT_PATH="/Users/eryxlee/Documents/idaddy/marketing/appstorescrapy"
SPIDER_ARR=(
    "appstore360"
    "appstorebaidu"
    "appstoremyapp"
    "appstorewandoujia"
    "appstorehiapk"
    "appstore91"
    "appstorevmall"
    "appstorelenovo"
    )

cd ${PROJECT_PATH}
for i in ${SPIDER_ARR[@]}
do
   `${SCRAPY} crawl ${i}`
done

