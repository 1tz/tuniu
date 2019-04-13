# -*- coding: utf-8 -*-
import os
import time
import json
import scrapy
from fake_useragent import UserAgent
from tuniu.items import Review


class ReviewSpider(scrapy.Spider):
    name = 'review'
    allowed_domains = ['tuniu.com']
    
    tuniu_url = 'http://tuniu.com/'

    def get_headers(self):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
            'dnt': 1,
            'upgrade-insecure-requests': 1,
            'user-agent': str(UserAgent().random)
        }
        return headers

    def start_requests(self):
        '''程序入口，开始爬取全球目的地
        '''
        yield scrapy.Request(url='http://www.tuniu.com/place/', 
            callback=self.get_nation_urls,
            headers=self.get_headers())

    def get_nation_urls(self, response):
        '''获取全球目的地国家链接
        '''
        urls = response.xpath('//ul[@class="col"]/li/a/@href').extract()
        yield scrapy.Request(url=urls[12],
            callback=self.switch_tag_to_destination,
            headers=self.get_headers())
        # for destination_urls in response.xpath('//ul[@class="col"]/li/a/@href').extract():
        #     yield scrapy.Request(url=destination_urls,
        #         callback=self.switch_tag_to_destination,
        #         headers=self.get_headers())

    def switch_tag_to_destination(self, response):
        '''切换到目的地城市链接
        '''
        switch_tag_url = self.tuniu_url + response.xpath('//ul[@class="cf"]/li[3]/a/@href').extract_first()
        yield scrapy.Request(url=switch_tag_url,
            callback=self.get_city_page,
            headers=self.get_headers())
        
    def get_city_page(self, response):
        '''获取城市页数，并发送请求
        '''
        num_citys = int(response.xpath('//div[@id="list"]/h2/a/text()').extract_first())
        poiId = response.url.split('/')[-3].split('-')[-1]
        max_page = int((num_citys - 1)) / 12 + 1
        for cur_page in range(1, max_page + 1):
            unix_time_stamp = str(self.get_unix_time_stamp())
            url = self.tuniu_url + '/newguide/api/widget/render/?widget=guide.HotDestinationWidget&params%5BpoiId%5D=' + poiId + '&params%5Bpage%5D=' + str(cur_page) + '&_=' + unix_time_stamp
            yield scrapy.Request(url=url,
                callback=self.get_city_urls,
                headers=self.get_headers())
    
    def get_city_urls(self, response):
        '''获取指定一页目的地城市链接
        '''
        html_string = json.loads(response.text)['data']
        html = lxml.html.fromstring(html_string)
        for city_url in doc.xpath('//a[@class="main"]/@href'):
            city_url = self.tuniu_url + city_url
            yield scrapy.Request(url=city_url,
                callback=self.switch_tag_to_review,
                headers=self.get_headers())

    def switch_tag_to_review(self, response):
        '''切换到某城市的景点标签下
        '''
        last_forth_tag = response.xpath('//ul[@class="cf"]/li[last()-3]/a/text()').extract_first()
        if last_forth_tag == '点评':
            last_forth_tag_url = self.tuniu_url + response.xpath('//ul[@class="cf"]/li[last()-3]/a/@href').extract_first()
            yield scrapy.Request(url=last_forth_tag_url,
                callback=self.get_review_urls,
                headers=self.get_headers())
