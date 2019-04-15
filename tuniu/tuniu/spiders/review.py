# -*- coding: utf-8 -*-
import os
import time
import json
import scrapy
import lxml.html
from lxml import etree
from fake_useragent import UserAgent
from tuniu.items import Review


class ReviewSpider(scrapy.Spider):
    name = 'review'
    allowed_domains = ['tuniu.com']
    
    tuniu_url = 'http://tuniu.com/'

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
                callback=self.switch_tag_to_comment,
                headers=self.get_headers())

    def switch_tag_to_comment(self, response):
        '''切换到评论链接
        '''
        switch_tag_url = response.xpath('//div[@class="interact wrapper"]/div[@class="summary"]/a/@href').extract_first()
        if switch_tag_url != None:
            switch_tag_url = self.tuniu_url + switch_tag_url
            yield scrapy.Request(url=switch_tag_url,
                callback=self.get_comment_page,
                headers=self.get_headers())
        
    def get_comment_page(self, response):
        '''获取评论页数，并发送请求
        '''
        num_comments = int(response.xpath('//span[@class="header-comment-total"]/text()').extract_first())
        nation_rate = float(response.xpath('//span[@class="header-mark"]/text()').extract_first())
        poiId = response.url.split('/')[-3].split('-')[-1]
        max_page = int((num_comments - 1) / 10) + 1
        for cur_page in range(1, max_page + 1):
            unix_time_stamp = str(self.get_unix_time_stamp())
            url = self.tuniu_url + '/newguide/api/widget/render/?widget=comment.CommentModuleWidget&params%5BpoiId%5D=' + poiId + '&params%5Bpage%5D=' + str(cur_page) + '&params%5Bsort%5D%5B%5D=default&params%5Bsort%5D%5B%5D=DESC&params%5BreplyCheck%5D=0&_=' + unix_time_stamp
            yield scrapy.Request(url=url,
                meta={'nation_rate': nation_rate},
                callback=self.get_review,
                headers=self.get_headers())
    
    def get_review(self, response):
        '''解析评论
        '''
        raw_html = response.text[24:-2].replace('\\', '')
        html = lxml.html.fromstring(raw_html)
        for review_div in html.xpath('//div[@class="item"]'):
            if review_div.xpath('div[2]/div[1]/p[2]/span[2]/text()')[0] == '景点':
                review = Review()
                review['spot_id'] = review_div.xpath('div[2]/div[1]/p[1]/span[2]/a/@href')[0].split('/')[1]
                review['spot_nation_rate'] = response.meta['nation_rate']
                review['nickname'] = review_div.xpath('div[2]/div[1]/p[1]/span[1]/text()')[0]
                review['spot_name'] = review_div.xpath('div[2]/div[1]/p[1]/span[2]/a/text()')[0]
                star = list(review_div.xpath('div[2]/div[1]/p[2]/span[1]')[0].classes)[1]
                review['review_time'] = review_div.xpath('div[2]/div[1]/p[1]/span[3]/text()')[0]
                review['rate'] = int(star.split('-')[-1])
                review['desc'] = review_div.xpath('div[2]/div[2]/text()')[0]
                review['upvote'] = int(review_div.xpath('div[2]/div[3]/p[1]/span/text()')[0])
                review['num_reply'] = int(review_div.xpath('div[2]/div[3]/p[2]/span/text()')[0])
                yield review
