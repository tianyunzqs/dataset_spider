# -*- coding: utf-8 -*-
# @Time        : 2020/7/10 18:02
# @Author      : tianyunzqs
# @Description : 

from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

execute(['scrapy', 'crawl', 'xzqh_spider'])


# # -*-coding:utf-8-*-
#
# import requests
#
# headers = {
#     'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE'
# }
# response_1=requests.get("https://www.youbianku.com/%E8%A1%A1%E6%B0%B4", headers=headers)
#
# print(response_1.text)

