# -*- coding: utf-8 -*-
import os
import time
import json
import scrapy
import lxml.html
from fake_useragent import UserAgent
from tuniu.items import Spot

class SpotSpider(scrapy.Spider):
    name = 'spot'
    allowed_domains = ['tuniu.com']

    tuniu_url = 'http://www.tuniu.com'

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

    def get_unix_time_stamp(self):
        return int(round(time.time() * 1000))

    def start_requests(self):
        '''程序入口，开始爬取全球目的地
        '''
        yield scrapy.Request(url='http://www.tuniu.com/place/', 
            callback=self.get_nation_urls,
            headers=self.get_headers())

    def get_nation_urls(self, response):
        '''获取全球目的地国家链接
        '''
        for destination_urls in response.xpath('//ul[@class="col"]/li/a/@href').extract():
            yield scrapy.Request(url=destination_urls,
                callback=self.switch_tag_to_destination,
                headers=self.get_headers())

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
        num_citys = response.xpath('//div[@id="list"]/h2/a/text()').extract_first()
        if num_citys != None:
            num_citys = int(num_citys)
            poiId = response.url.split('/')[-3].split('-')[-1]
            max_page = int((num_citys - 1) / 12) + 1
            for cur_page in range(1, max_page + 1):
                unix_time_stamp = str(self.get_unix_time_stamp())
                url = self.tuniu_url + '/newguide/api/widget/render/?widget=guide.HotDestinationWidget&params%5BpoiId%5D=' + poiId + '&params%5Bpage%5D=' + str(cur_page) + '&_=' + unix_time_stamp
                yield scrapy.Request(url=url,
                    callback=self.get_city_urls,
                    headers=self.get_headers())
    
    def get_city_urls(self, response):
        '''获取指定一页目的地城市链接
        '''
        html = lxml.html.fromstring(response.text[24:-2])
        for city_url in html.xpath('//a[@class="main"]/@href'):
            city_url = self.tuniu_url + city_url
            yield scrapy.Request(url=city_url,
                callback=self.switch_tag_to_spot,
                headers=self.get_headers())

    def switch_tag_to_spot(self, response):
        '''切换到某城市的景点标签下
        '''
        city = response.xpath('//div[@class="f_left"]/h1/text()').extract_first()
        third_tag = response.xpath('//ul[@class="cf"]/li[3]/a/text()').extract_first()
        if third_tag == '景点':
            third_tag_url = self.tuniu_url + response.xpath('//ul[@class="cf"]/li[3]/a/@href').extract_first()
            yield scrapy.Request(url=third_tag_url,
                meta={'city': city},
                callback=self.get_spot_urls,
                headers=self.get_headers())

    def get_spot_urls(self, response):
        '''获取某城市所有景点连接，这里有翻页
        '''
        for spot_url in response.xpath('//div[@class="allSpots"]/ul/li/a/@href').extract():
            spot_url = self.tuniu_url + spot_url
            yield scrapy.Request(url=spot_url,
                meta={'city': response.meta['city']},
                callback=self.sparse_spot,
                headers=self.get_headers())
        if response.xpath('//div[@class="page-bottom"]/a[last()]/text()').extract_first() == '下一页':
            next_url = self.tuniu_url + response.xpath('//div[@class="page-bottom"]/a[last()]/@href').extract_first()
            yield scrapy.Request(url=next_url,
                meta={'city': response.meta['city']},
                callback=self.get_spot_urls,
                headers=self.get_headers())

    def sparse_spot(self, response):
        '''解析景点信息
        '''
        spot = Spot()
        spot['id'] = response.url.split('/')[-3]
        spot['name'] = response.xpath('//h1[@class="signal"]/text()').extract_first()
        spot['city'] = response.meta['city']
        spot['desc'] = response.xpath('//div[@class="coat"]/p/text()').extract_first()
        spot['addr'] = response.xpath('//div[@class="route"]/div[1]/div[2]/text()').extract_first()
        spot['open_time'] = response.xpath('//div[@class="route"]/div[2]/div[2]/text()').extract_first()
        traffic_names = response.xpath('//p[@class="traffic-name"]/text()').extract()
        traffic_mentions = response.xpath('//p[@class="traffic-mention"]/text()').extract()
        traffic_dict = dict((name, mention) for name, mention in zip(traffic_names,traffic_mentions))
        spot['traffic'] = traffic_dict
        spot['rec_play_time'] = response.xpath('//div[@class="content far"]/div[2]/text()').extract_first()
        must_site_urls = response.xpath('//div[@class="site-distance"]/div[1]/div/div/a/@href').extract()
        must_site_ids = [url.split('/')[1] for url in must_site_urls]
        must_site_dists = response.xpath('//div[@class="site-distance"]/div[1]/div/div/span/text()').extract()
        must_site_dict = dict((i, dist) for i, dist in zip(must_site_ids, must_site_dists))
        near_site_urls = response.xpath('//div[@class="site-distance"]/div[2]/div/div/a/@href').extract()
        near_site_ids = [url.split('/')[1] for url in must_site_urls]
        near_site_dists = response.xpath('//div[@class="site-distance"]/div[2]/div/div/span/text()').extract()
        near_site_dict = dict((i, dist) for i, dist in zip(must_site_ids, must_site_dists))
        spot['site_dist'] = {'must': must_site_dict, 'near': near_site_dict}
        yield spot
