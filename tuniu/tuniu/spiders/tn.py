# -*- coding: utf-8 -*-
import time
import scrapy
from fake_useragent import UserAgent
from tuniu.items import Spot, Review

class TnSpider(scrapy.Spider):
    name = 'tn'
    allowed_domains = ['tuniu.com']

    custom_settings = {
        "ROBOTSTXT_OBEY": False  # 需要忽略ROBOTS.TXT文件
    }

    tuniu_url = 'http://www.tuniu.com'

    def start_requests(self):
        '''程序入口，开始爬取全球目的地
        '''
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
            'dnt': 1,
            'upgrade-insecure-requests': 1,
            'user-agent': str(UserAgent().random)
        }
        yield scrapy.Request(url='http://www.tuniu.com/place/', 
            callback=self.get_nation_urls,
            headers=self.headers)

    def get_nation_urls(self, response):
        '''获取全球目的地国家链接
        '''
        urls = response.xpath('//ul[@class="col"]/li/a/@href').extract()
        yield scrapy.Request(url=urls[12],
            callback=self.switch_tag_to_destination,
            headers=self.headers)
        # for destination_urls in response.xpath('//ul[@class="col"]/li/a/@href').extract():
        #     yield scrapy.Request(url=destination_urls,
        #         callback=self.parse_jump_to_citys,
        #         headers=self.headers)

    def switch_tag_to_destination(self, response):
        '''切换到目的地城市链接
        '''
        switch_tag_url = self.tuniu_url + response.xpath('//ul[@class="cf"]/li[3]/a/@href').extract_first()
        yield scrapy.Request(url=switch_tag_url,
            callback=self.get_city_urls,
            headers=self.headers)
        
    def get_city_urls(self, response):
        '''获取目的地城市链接，这里有可能会有翻页
        '''
        for city_url in response.xpath('//div[@id="list"]/ul/li/a/@href').extract():
            city_url = self.tuniu_url + city_url
            yield scrapy.Request(url=city_url,
                callback=self.switch_tag_to_spot,
                headers=self.headers)

    def switch_tag_to_spot(self, response):
        '''切换到某城市的景点标签下
        '''
        third_tag = response.xpath('//ul[@class="cf"]/li[3]/a/text()').extract_first()
        if third_tag == '景点':
            third_tag_url = self.tuniu_url + response.xpath('//ul[@class="cf"]/li[3]/a/@href').extract_first()
            time.sleep(2)
            yield scrapy.Request(url=third_tag_url,
                callback=self.get_spot_urls,
                headers=self.headers)

    def get_spot_urls(self, response):
        '''获取某城市所有景点连接，这里可能会有翻页
        '''
        for spot_url in response.xpath('//div[@class="allSpots"]/ul/li/a/@href').extract():
            spot_url = self.tuniu_url + spot_url
            yield scrapy.Request(url=spot_url,
                callback=self.sparse_spot,
                headers=self.headers)

    def sparse_spot(self, response):
        '''解析景点信息
        '''
        spot = Spot()
        spot['name'] = response.xpath('//h1[@class="signal"]/text()').extract_first()
        spot['desc'] = response.xpath('//div[@class="coat"]/p/text()').extract_first()
        spot['addr'] = response.xpath('//div[@class="route"]/div[1]/div[2]/text()').extract_first()
        spot['open_time'] = response.xpath('//div[@class="route"]/div[2]/div[2]/text()').extract_first()
        traffic_names = response.xpath('//p[@class="traffic-name"]/text()').extract()
        traffic_mentions = response.xpath('//p[@class="traffic-mention"]/text()').extract()
        traffic = zip(traffic_names,traffic_mentions)
        traffic_dict = dict((name, mention) for name, mention in traffic)
        spot['traffic'] = traffic_dict
        spot['rec_play_time'] = response.xpath('//div[@class="content far"]/div[2]/text()').extract_first()
        # spot['location'] = response.xpath('')
        print(spot['name'])
        print(spot['desc'])
        print(spot['addr'])
        print(spot['open_time'])
        print(spot['traffic'])
        print(spot['rec_play_time'])





