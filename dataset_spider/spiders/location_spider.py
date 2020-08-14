# -*- coding: utf-8 -*-
# @Time        : 2020/7/10 17:25
# @Author      : tianyunzqs
# @Description : 

import re
import scrapy
from scrapy.http import Request
from bs4 import BeautifulSoup
from dataset_spider.items import DatasetSpiderItem, LocationItem
import sys


class LocationSpider(scrapy.Spider):
    """
    name: scrapy唯一定位实例的属性，必须唯一
    allowed_domains：允许爬取的域名列表，不设置表示允许爬取所有
    start_urls：起始爬取列表
    start_requests：它就是从start_urls中读取链接，然后使用make_requests_from_url生成Request，
                    这就意味我们可以在start_requests方法中根据我们自己的需求往start_urls中写入
                    我们自定义的规律的链接
    parse：回调函数，处理response并返回处理后的数据和需要跟进的url
    log：打印日志信息
    closed：关闭spider
    """
    # 设置name，scrapy唯一定位实例的属性，必须唯一
    name = "location_spider"
    # 设定域名，允许爬取的域名列表，不设置表示允许爬取所有
    allowed_domains = ['alexa.ip138.com']
    # 填写爬取地址，起始爬取列表
    # start_urls = [
    #     "https://www.shujukuji.cn/shenfenzhengdiqudaima/liebiao",
    # ]
    start_urls = [
        "https://www.youbianku.com/%E5%8C%97%E4%BA%AC",
        "http://alexa.ip138.com/post"
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    }

    urls = [
        {'province': '安徽省', 'url': 'http://alexa.ip138.com/post/anhui/'},
        {'province': '北京市', 'url': 'http://alexa.ip138.com/post/beijing/'},
        {'province': '福建省', 'url': 'http://alexa.ip138.com/post/fujian/'},
        {'province': '甘肃省', 'url': 'http://alexa.ip138.com/post/gansu/'},
        {'province': '广东省', 'url': 'http://alexa.ip138.com/post/guangdong/'},
        {'province': '广西壮族自治区', 'url': 'http://alexa.ip138.com/post/guangxi/'},
        {'province': '贵州省', 'url': 'http://alexa.ip138.com/post/guizhou/'},
        {'province': '海南省', 'url': 'http://alexa.ip138.com/post/hainan/'},
        {'province': '河北省', 'url': 'http://alexa.ip138.com/post/hebei/'},
        {'province': '河南省', 'url': 'http://alexa.ip138.com/post/henan/'},
        {'province': '黑龙江省', 'url': 'http://alexa.ip138.com/post/heilongjiang/'},
        {'province': '湖北省', 'url': 'http://alexa.ip138.com/post/hubei/'},
        {'province': '湖南省', 'url': 'http://alexa.ip138.com/post/hunan/'},
        {'province': '吉林省', 'url': 'http://alexa.ip138.com/post/jilin/'},
        {'province': '江苏省', 'url': 'http://alexa.ip138.com/post/jiangsu/'},
        {'province': '江西省', 'url': 'http://alexa.ip138.com/post/jiangxi/'},
        {'province': '辽宁省', 'url': 'http://alexa.ip138.com/post/liaoning/'},
        {'province': '内蒙古自治区', 'url': 'http://alexa.ip138.com/post/neimenggu/'},
        {'province': '宁夏回族自治区', 'url': 'http://alexa.ip138.com/post/ningxia/'},
        {'province': '青海省', 'url': 'http://alexa.ip138.com/post/qinghai/'},
        {'province': '山东省', 'url': 'http://alexa.ip138.com/post/shandong/'},
        {'province': '陕西省', 'url': 'http://alexa.ip138.com/post/shanxi/'},
        {'province': '上海市', 'url': 'http://alexa.ip138.com/post/shanghai/'},
        {'province': '四川省', 'url': 'http://alexa.ip138.com/post/sichuan/'},
        {'province': '天津市', 'url': 'http://alexa.ip138.com/post/tianjin/'},
        {'province': '西藏自治区', 'url': 'http://alexa.ip138.com/post/xizang/'},
        {'province': '新疆维吾尔自治区', 'url': 'http://alexa.ip138.com/post/xinjiang/'},
        {'province': '云南省', 'url': 'http://alexa.ip138.com/post/yunnan/'},
        {'province': '浙江省', 'url': 'http://alexa.ip138.com/post/zhejiang/'},
        {'province': '重庆市', 'url': 'http://alexa.ip138.com/post/chongqing/'},
        {'province': '山西省', 'url': 'http://alexa.ip138.com/post/shanx/'},
        {'province': '香港特别行政区', 'url': 'http://alexa.ip138.com/post/xianggang/'},
        {'province': '澳门特别行政区', 'url': 'http://alexa.ip138.com/post/aomen/'},
        {'province': '台湾', 'url': 'http://alexa.ip138.com/post/taiwang/'}
    ]
    i = 0
    city_name = ''

    def start_requests(self):
        return [Request(url=self.urls[self.i]['url'], callback=self.parse_province, headers=self.headers)]

    # 编写爬取方法
    def parse(self, response):
        result = []
        for line in response.xpath("//div[@id='newAlexa']/table/tr/td/a"):

            soup = BeautifulSoup(line.extract())
            item = {
                'province_name': soup.text,
                'area': []
            }
            href = "http://alexa.ip138.com" + soup.find('a').get('href')
            result.append({'province': soup.text, 'url': href})
        print(result)
            # yield Request(url=href, meta={'item': item}, callback=self.parse_province, headers=self.headers)
            # result.append(item)
        # print(result)

    @staticmethod
    def parse_province0(response):
        item = response.meta['item']
        tmp = {
            'area_name': '',
            'post_code': '',
            'area_code': ''
        }
        for line in response.xpath("//table[@class='t12']/tr/td"):
            soup = BeautifulSoup(line.extract())
            text = soup.text
            if text in ['市、县、区名', '邮政编码', '长途区号']:
                continue
            if re.search(r'[\u4e00-\u9fa5]+', text):
                tmp['area_name'] = text
            elif re.search(r'[0-9]{6,}', text):
                tmp['post_code'] = text
            elif re.search(r'[0-9]{3,5}', text):
                tmp['area_code'] = text
                item['area'].append(tmp)
                tmp = {
                    'area_name': '',
                    'post_code': '',
                    'area_code': ''
                }
        yield item

    def parse_province(self, response):
        item = LocationItem()
        item['province_name'] = self.urls[self.i]['province']
        for line in response.xpath("//table[@class='t12']/tr/td"):
            soup = BeautifulSoup(line.extract(), features="lxml")
            text = soup.text
            if text in ['市、县、区名', '邮政编码', '长途区号']:
                continue
            if re.search(r'[\u4e00-\u9fa5]+', text):
                item['location_name'] = text
                if soup.find('b'):
                    self.city_name = text
            elif re.search(r'[0-9]{6,}', text):
                item['post_code'] = text
            elif re.search(r'[0-9]{3,5}', text):
                item['area_code'] = text
                item['city_name'] = self.city_name
                yield item
                item = LocationItem()
                item['province_name'] = self.urls[self.i]['province']
        self.i += 1
        yield Request(url=self.urls[self.i]['url'], callback=self.parse_province, headers=self.headers)
