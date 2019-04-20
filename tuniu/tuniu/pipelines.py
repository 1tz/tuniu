# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from tuniu.spiders.spot import SpotSpider
from tuniu.spiders.review import ReviewSpider
from tuniu.spiders.recap import RecapSpider
from tuniu.items import Spot, Review

class TuniuPipeline(object):

    def open_spider(self, spider):
        '''开始运行爬虫时，按续写方式打开文件'''
        if isinstance(spider, SpotSpider):
            self.spot_file = open('spot.json', 'a', encoding='utf-8')
        elif isinstance(spider, ReviewSpider):
            self.review_file = open('review.json', 'a', encoding='utf-8')
        elif isinstance(spider, RecapSpider):
            self.recap_file = open('recap.json', 'a', encoding='utf-8')

    def close_spider(self, spider):
        '''爬虫结束时，关闭文件'''
        if isinstance(spider, SpotSpider):
            self.spot_file.close()
        elif isinstance(spider, ReviewSpider):
            self.review_file.close()
        elif isinstance(spider, RecapSpider):
            self.recap_file.close()

    def process_item(self, item, spider):
        '''将item转为字符串格式写入对应文件中'''
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        if isinstance(spider, SpotSpider):
            self.spot_file.write(line)
        elif isinstance(spider, ReviewSpider):
            self.review_file.write(line)
        elif isinstance(spider, RecapSpider):
            self.recap_file.write(line)
        return item
