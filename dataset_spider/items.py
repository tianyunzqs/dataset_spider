# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DatasetSpiderItem(scrapy.Item):
    # 地区名称
    province_name = scrapy.Field()
    location_name = scrapy.Field()
    # 地区代码（中国公民身份证前六位编码）
    post_code = scrapy.Field()
    area_code = scrapy.Field()


class LocationItem(scrapy.Item):
    province_name = scrapy.Field()
    city_name = scrapy.Field()
    location_name = scrapy.Field()
    post_code = scrapy.Field()
    area_code = scrapy.Field()
    is_city = scrapy.Field()


class XZQHItem(scrapy.Item):
    # 省
    province_name = scrapy.Field()
    # 市
    city_name = scrapy.Field()
    # 区/县
    county_name = scrapy.Field()
    # 驻地
    station = scrapy.Field()
    # 人口
    population = scrapy.Field()
    # 面积
    area_size = scrapy.Field()
    # 行政区划代码
    administrative_code = scrapy.Field()
    # 区号
    area_code = scrapy.Field()
    # 邮编
    post_code = scrapy.Field()
