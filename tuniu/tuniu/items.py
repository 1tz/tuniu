# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Spot(scrapy.Item):
    '''景点
    name 景点名称
    desc 景点描述
    addr 景点详细地址
    open_time 景点开放时间
    ref_play_time 推荐游玩时长
    traffic 交通信息
    location 与必玩景点、附近景点距离
    '''
    id = scrapy.Field()
    name = scrapy.Field()
    desc = scrapy.Field()
    addr = scrapy.Field()
    open_time = scrapy.Field()
    traffic = scrapy.Field()
    rec_play_time = scrapy.Field()
    location = scrapy.Field()

class Review(scrapy.Item):
    '''评论
    nickname 昵称
    attraction 景点名称
    rate 评分
    desc 用户评分描述
    '''
    nickname = scrapy.Field()
    attraction = scrapy.Field()
    rate = scrapy.Field()
    desc = scrapy.Field()
