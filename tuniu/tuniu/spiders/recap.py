# -*- coding: utf-8 -*-
import os
import time
import json
import scrapy
import lxml.html
from fake_useragent import UserAgent
from tuniu.items import Spot


class RecapSpider(scrapy.Spider):
    name = 'recap'
    allowed_domains = ['tuniu.com']
    start_urls = ['http://tuniu.com/']

    def get_headers(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
            'DNT': 1,
            'Connection': 'keep-alive',
            'Host': 'www.tuniu.com',
            'Upgrade-Insecure-Requests': 1,
            'User-Agent': str(UserAgent().random)
        }
        return headers

    def start_requests(self):
        '''程序入口，开始爬取全球目的地
        '''
        with open('recapurl.json', 'r', encoding='utf8') as f:
            for line in f:
                spot = json.loads(line)
                yield scrapy.Request(url=spot['url'], 
                    meta={'city': spot['city'], 'nation': spot['nation']},
                    callback=self.sparse_spot,
                    headers=self.get_headers())

    def sparse_spot(self, response):
        '''解析景点信息
        '''
        spot = Spot()
        spot['id'] = response.url.split('/')[-3]
        spot['name'] = response.xpath('//h1[@class="signal"]/text()').extract_first()
        spot['nation'] = response.meta['nation']
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
