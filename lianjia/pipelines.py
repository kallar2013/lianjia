# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
from scrapy.conf import settings

class SqlitePipeline(object):
    
    def __init__(self):
        self.conn = sqlite3.connect(settings['DB_NAME'])
        self.conn.text_factory = str
        self.cur = self.conn.cursor()
        
    def process_item(self, item, spider):
        if spider.name == 'xq_sh':
            self.do_insert_xq(item)
        elif spider.name == 'cj_sh':
            self.do_insert_cj(item)
        else:
            print('Do not need to insert')
            return
        
    def do_insert_xq(self, item):
        str_tag = settings['XIAOQU_STR']
        qmark = ','.join(len(str_tag) * ['?'])
        cols = '"' + '","'.join(str_tag) + '"'
        sql = 'INSERT INTO xiaoqu (%s) VALUES (%s)' % (cols, qmark)
        data = (item.get('mid', ''), item.get('title', ''), item.get('year', ''), item.get('ditie', ''), 
            item.get('price', ''), item.get('onsale', ''), item.get('platename', ''), item.get('district', ''), 
            item.get('city', ''), item.get('coordinate', ''))
        self.cur.execute(sql, data)
        self.conn.commit()
    def do_insert_cj(self, item):
        str_tag = settings['CHENGJIAO_STR']
        qmark = ','.join(len(str_tag) * ['?'])
        cols = '"' + '","'.join(str_tag) + '"'
        sql = 'INSERT INTO chengjiao (%s) VALUES (%s)' % (cols, qmark)
        data = (item.get('mid', ''), item.get('xq_name', ''),item.get('house_type', ''),  item.get('size', ''),
            item.get('storey', ''), item.get('orientation', ''), item.get('decoration', ''), item.get('subway', ''), item.get('five_year', ''), 
            item.get('two_year', ''), item.get('deal_date', ''), item.get('unit_price', ''), item.get('total_price', ''))
        self.cur.execute(sql, data)
        self.conn.commit()
    
    def closeDB(self):
        self.conn.close()
    
    def __del__(self):
        self.closeDB()
