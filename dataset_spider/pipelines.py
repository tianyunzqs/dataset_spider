# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import MySQLdb


class DatasetSpiderPipeline:
    def __init__(self):
        self.conn = MySQLdb.connect('host', 'user', 'password', 'database', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()
        # self.filename = open("xx.json", "w", encoding='utf-8')

    def process_item(self, item, spider):
        pass
        # jsontext = str(json.dumps(dict(item), ensure_ascii=False)) + "\n"
        # self.filename.write(jsontext)
        # return item
        insert_sql = """
            insert into xzqhxxb(province_name, city_name, county_name, station, population, area_size, 
            administrative_code, area_code, post_code)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (
            item["province_name"], item["city_name"], item["county_name"] if 'county_name' in item else '',
            item["station"], item["population"],
            item["area_size"], item["administrative_code"], item["area_code"], item["post_code"]))
        self.conn.commit()

    def close_spider(self, spider):
        # self.filename.close()
        self.conn.close()
