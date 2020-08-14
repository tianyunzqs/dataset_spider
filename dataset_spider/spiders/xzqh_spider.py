# -*- coding: utf-8 -*-
# @Time        : 2020/8/5 16:37
# @Author      : tianyunzqs
# @Description : 

import re
import scrapy
from urllib import request, parse
from scrapy.http import Request
from bs4 import BeautifulSoup
from dataset_spider.items import XZQHItem


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
    name = "xzqh_spider"
    # 设定域名，允许爬取的域名列表，不设置表示允许爬取所有
    allowed_domains = ['xzqh.mca.gov.cn']
    # 填写爬取地址，起始爬取列表
    start_urls = [
        'http://xzqh.mca.gov.cn/defaultQuery?'
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
    }

    shengji = [
        "北京市(京)",
        "天津市(津)",
        "河北省(冀)",
        "山西省(晋)",
        "内蒙古自治区(内蒙古)",
        "辽宁省(辽)",
        "吉林省(吉)",
        "黑龙江省(黑)",
        "上海市(沪)",
        "江苏省(苏)",
        "浙江省(浙)",
        "安徽省(皖)",
        "福建省(闽)",
        "江西省(赣)",
        "山东省(鲁)",
        "河南省(豫)",
        "湖北省(鄂)",
        "湖南省(湘)",
        "广东省(粤)",
        "广西壮族自治区(桂)",
        "海南省(琼)",
        "重庆市(渝)",
        "四川省(川、蜀)",
        "贵州省(黔、贵)",
        "云南省(滇、云)",
        "西藏自治区(藏)",
        "陕西省(陕、秦)",
        "甘肃省(甘、陇)",
        "青海省(青)",
        "宁夏回族自治区(宁)",
        "新疆维吾尔自治区(新)",
        "香港特别行政区(港)",
        "澳门特别行政区(澳)",
        "台湾省(台)"
    ]
    i = 0
    city = ''

    def start_requests(self):
        return [Request(
            url=self.start_urls[0] + 'shengji={0}&diji=-1&xianji=-1'.format(parse.quote(self.shengji[self.i], encoding='gbk')),
            callback=self.parse,
            headers=self.headers)
        ]

    # 编写爬取方法
    def parse(self, response):
        print(self.shengji[self.i])
        j = 0
        tmp_result = XZQHItem()
        lines = response.xpath("//table[@class='info_table']/tr/td")
        while j < len(lines):
            soup = BeautifulSoup(lines[j].extract())
            try:
                self.city = soup.find('a', {'class': 'name_text'}).text
            except:
                pass

            if soup.find('td', {'class': 'name_left'}) and [v for _, v in tmp_result.items() if v]:
                yield tmp_result
                tmp_result = XZQHItem()
                if '+' not in soup.text.strip():
                    tmp_result['county_name'] = soup.text.strip()
            else:
                tmp_result['province_name'] = re.sub(r'\(.*?\)', '', self.shengji[self.i])
                tmp_result['city_name'] = self.city
                if j % 7 == 0:  # 区县
                    if len([v for _, v in tmp_result.items() if v]) == 9:
                        yield tmp_result
                        tmp_result = XZQHItem()
                    if '+' not in soup.text.strip():
                        tmp_result['county_name'] = soup.text.strip()
                elif j % 7 == 1:  # 驻地
                    tmp_result['station'] = soup.text.strip()
                elif j % 7 == 2:  # 人口
                    tmp_result['population'] = soup.text.strip()
                elif j % 7 == 3:  # 面积
                    tmp_result['area_size'] = soup.text.strip()
                elif j % 7 == 4:  # 行政区划代码
                    tmp_result['administrative_code'] = soup.text.strip()
                elif j % 7 == 5:  # 区号
                    tmp_result['area_code'] = soup.text.strip()
                elif j % 7 == 6:  # 邮编
                    tmp_result['post_code'] = soup.text.strip()
            j += 1
        if [v for _, v in tmp_result.items() if v]:
            yield tmp_result
        self.i += 1
        yield Request(
            url=self.start_urls[0] + 'shengji={0}&diji=-1&xianji=-1'.format(parse.quote(self.shengji[self.i], encoding='gbk')),
            callback=self.parse,
            headers=self.headers)
