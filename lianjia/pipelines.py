# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
import json
from scrapy.exceptions import DropItem
from scrapy.conf import settings
XIAOQU_STR_SH = ["小区ID", "小区名称", "建成年代", "地铁房", "小区均价", "在售二手房数量", "所在地点", "所在行政区", "所在城市", "坐标"]
CHENGJIAO_STR_SH = ('房源编号', "小区名称", "房屋户型", "建筑面积", "所在楼层", "房屋朝向",
        "装修情况", "地铁房", "满五年唯一", "房本满两年", "售出时间", "出售单价", "出售总价")
ERSHOUFANG_STR_SH = ('房源编号', '小区ID', '标题', '户型', '建造年代', '建筑面积', '房屋朝向', '所在楼层', '浏览人数', '满五唯一', '房本满两年', '有钥匙', '附近地铁', '总价', '单价', '爬虫时间')
XIAOQU_STR = ("小区ID", "小区名称", "户型数量", "30天成交", "90天成交", "在出租数量", "建筑类型", "建成年代", 
            "地铁房", "学区房", "小区均价", "在售二手房数量", "所在地点", "所在行政区", "所在城市")
CHENGJIAO_STR = ('房源编号', "小区名称", "小区ID", "房屋户型", "建筑面积", "所在楼层", "房屋朝向", "建筑类型", "建筑年代", 
            "装修情况", "地铁房", "学区房", "满五年唯一", "房本满两年", "配备电梯", "售出时间", "出售单价", "出售总价")
ERSHOUFANG_STR = ('房源编号', '标题', '小区ID', '户型', '建筑面积', '房屋朝向', '装修', '电梯', '所在楼层', '建造年代', '建筑类型',
            '关注人数', '带看次数', '发布时间', '满五唯一', '房本满两年', '附近小学', '附近地铁', '总价', '单价', '爬虫时间')
ZUFANG_STR = ("房源编号", "标题", "小区ID", "户型", "建筑面积", "房屋朝向", "所在楼层", "建成年代", "建筑类型", "看过此房人数",
            "最后更新时间", "附近地铁", "供暖", "精装修", "阳台", "独家", "租金每月", "其他标签", "爬虫时间")
            
class SqlitePipeline(object):
    
    def __init__(self):
        self.conn = sqlite3.connect(settings['DB_NAME'])
        self.conn.text_factory = str
        self.cur = self.conn.cursor()
        self.mids_seen_xq = set()
        self.mids_seen_esf = set()
        self.mids_seen_cj = set()
        self.mids_seen_zf = set()
        
    def process_item(self, item, spider):
        spiders = ['plate', 'xq', 'cj', 'esf', 'zf']
        if spider.name not in spiders:
            return
        funcs = [self.do_write_plate, self.do_insert_xq, self.do_insert_cj, self.do_insert_esf, self.do_insert_zf]
        func = dict(zip(spiders, funcs))[item.class_name]
        func(item, spider.city)
        
    def do_write_plate(self, item, city):
        with open('./plates/%s.dat' % city, 'a', encoding='utf-8') as f:
            f.write(json.dumps(dict(item)) + '\n')

    def do_insert_xq(self, item, city):
        if item['mid'] in self.mids_seen_xq:
            raise DropItem('mid duplicate found: %s, %s' % item['mid'], item.class_name)
        else:
            self.mids_seen_xq.add(item['mid'])
        if city == 'sh':
            return self.do_insert_xq_sh(item)
        else:
            str_tag = XIAOQU_STR
            qmark = ','.join(len(str_tag) * ['?'])
            cols = '"' + '","'.join(str_tag) + '"'
            sql = 'INSERT INTO xiaoqu (%s) VALUES (%s)' % (cols, qmark)
            data = (item.get('mid', ''), item.get('name', ''), item.get('house_type_num', ''), item.get('thirty_days', ''), 
                item.get('ninety_days', ''), item.get('onrent', ''), item.get('mtype', ''), item.get('built_year', ''), item.get('subway', ''), 
                item.get('school', ''), item.get('price'), item.get('onsale'), item.get('plate'), item.get('district'), item.get('city'))
            self.cur.execute(sql, data)
            self.conn.commit()

    def do_insert_cj(self, item, city):
        if item['mid'] in self.mids_seen_cj:
            raise DropItem('mid duplicate found: %s, %s' % item['mid'], item.class_name)
        else:
            self.mids_seen_cj.add(item['mid'])
        if city == 'sh':
            return self.do_insert_cj_sh(item)
        else:
            str_tag = CHENGJIAO_STR
            qmark = ','.join(len(str_tag) * ['?'])
            cols = '"' + '","'.join(str_tag) + '"'
            sql = 'INSERT INTO chengjiao (%s) VALUES (%s)' % (cols, qmark)
            
            data = (item.get('mid', ''), item.get('xq_name', ''), item.get('xq_id', ''), item.get('house_type', ''),  item.get('size', ''),
                item.get('storey', ''), item.get('orientation', ''), item.get('mtype', ''), item.get('built_year', ''), item.get('decoration', ''), 
                item.get('subway', ''), item.get('school', ''), item.get('five_year', ''), item.get('two_year', ''), 
                item.get('elevator', ''), item.get('deal_date', ''), item.get('unit_price', ''), item.get('total_price', ''))
            self.cur.execute(sql, data)
            self.conn.commit()
            
    def do_insert_esf(self, item, city):
        if item['mid'] in self.mids_seen_esf:
            raise DropItem('mid duplicate found: %s, %s' % item['mid'], item_class_name)
        else:
            self.mids_seen_esf.add(item['mid'])
        if city == 'sh':
            return self.do_insert_esf_sh(item)
        else:
            str_tag = ERSHOUFANG_STR
            qmark = ','.join(len(str_tag) * ['?'])
            cols = '"' + '","'.join(str_tag) + '"'
            sql = 'INSERT INTO ershoufang (%s) VALUES (%s)' % (cols, qmark)
            data = (item.get('mid', ''), item.get('title', ''), item.get('xq_id', ''),item.get('house_type', ''),  
                item.get('size', ''), item.get('orientation', ''), item.get('decoration', ''), item.get('elevator', ''), 
                item.get('storey', ''), item.get('built_year', ''), item.get('mtype', ''), item.get('focus', ''), item.get('visited', ''), 
                item.get('publish_date', ''), item.get('five_year', ''), item.get('two_year', ''), item.get('school', ''), 
                item.get('subway', ''), item.get('total_price', ''), item.get('unit_price', ''), item.get('crawl_date'))
            self.cur.execute(sql, data)
            self.conn.commit()
    
    def do_insert_zf(self, item, city):
        if item['mid'] in self.mids_seen_zf:
            raise DropItem('mid duplicate found: %s, %s' % item['mid'], item.class_name)
        else:
            self.mids_seen_zf.add(item['mid'])
        if city == 'sh':
            return self.do_insert_zf_sh(item)
        else:
            str_tag = ZUFANG_STR
            qmark = ','.join(len(str_tag) * ['?'])
            cols = '"' + '","'.join(str_tag) + '"'
            sql = 'INSERT INTO zufang (%s) VALUES (%s)' % (cols, qmark)
            data = (item.get('mid', ''), item.get('title', ''), item.get('xq_id', ''),item.get('house_type', ''),  
                item.get('size', ''), item.get('orientation', ''), item.get('storey', ''), item.get('built_year', ''), 
                item.get('mtype', ''), item.get('visited', ''), item.get('last_updated', ''), item.get('subway', ''), 
                item.get('heat', ''), item.get('decoration', ''), item.get('balcony', ''), item.get('only', ''), 
                item.get('rent', ''), item.get('other_tags', ''), item.get('crawl_date'))
            self.cur.execute(sql, data)
            self.conn.commit()
    
    # 以下是用来专门处理上海链家的数据
    def do_insert_esf_sh(self, item):
        str_tag = ERSHOUFANG_STR_SH
        qmark = ','.join(len(str_tag) * ['?'])
        cols = '"' + '","'.join(str_tag) + '"'
        sql = 'INSERT INTO ershoufang (%s) VALUES (%s)' % (cols, qmark)
        data = (item.get('mid'), item.get('xq_id'), item.get('title'), item.get('house_type'), item.get('built_year'), 
            item.get('size'), item.get('orientation'), item.get('storey'), item.get('visited'), item.get('five_year'),
            item.get('two_year'), item.get('haskey'), item.get('subway'), item.get('total_price'), item.get('unit_price'),
            item.get('crawl_date'))
        self.cur.execute(sql, data)
        self.conn.commit()
    
    def do_insert_xq_sh(self, item):
        str_tag = XIAOQU_STR_SH
        qmark = ','.join(len(str_tag) * ['?'])
        cols = '"' + '","'.join(str_tag) + '"'
        sql = 'INSERT INTO xiaoqu (%s) VALUES (%s)' % (cols, qmark)
        data = (item.get('mid', ''), item.get('title', ''), item.get('year', ''), item.get('ditie', ''), 
            item.get('price', ''), item.get('onsale', ''), item.get('platename', ''), item.get('district', ''), 
            item.get('city', ''), item.get('coordinate', ''))
        self.cur.execute(sql, data)
        self.conn.commit()
        
    def do_insert_cj_sh(self, item):
        str_tag = CHENGJIAO_STR_SH
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
