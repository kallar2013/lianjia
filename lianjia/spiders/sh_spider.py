import scrapy
from scrapy.spiders import Spider
import lianjia.parsers as parser
from lianjia.items import Xiaoqu, Chengjiao, Plate
from scrapy import Request
import re
import json

def get_plate_urls(base_url):
    urls = set()
    with open('./plates.dat', 'r') as f:
        for line in f.readlines():
            urls.add(base_url + json.loads(line)['url'])
    return list(urls)
    
class EsfSpider(Spider):
    name = 'esf_sh'
    base_url = 'http://sh.lianjia.com/ershoufang/'
    allowed_domains = ['lianjia.com', ]
    start_urls = get_plate_urls(base_url)
    
    def parse(self, response):
        for li in response.xpath('//ul[@id="house-lst"]/li'):
            item = parser.ershoufang_sh(li)
            yield item
        # link to next page    
        next_page_href = ''.join(response.css('a[gahref="results_next_page"]::attr(href)').re('/ershoufang/([0-9a-z]+/d[0-9]+)'))
        if not next_page_href:
            return
        next_page_url = self.base_url + next_page_href
        yield Request(next_page_url)
        
class CjSpider(Spider):
    name = 'cj_sh'
    base_url = 'http://sh.lianjia.com/chengjiao/'
    
    start_urls = [base_url, ]
    
    auth_url = 'https://passport.lianjia.com/cas/login?service=http%3A%2F%2Fbj.lianjia.com%2F'
    allowed_domains = ['lianjia.com']
    
    def start_requests(self):
        return [Request(self.auth_url, callback=self.pre_login)]
    
    def pre_login(self, response):
        pattern = re.compile(r'value=\"(LT-.*)\"')
        lt = pattern.findall(response.text)[0]
        
        pattern = re.compile(r'name="execution" value="(.*)"')
        execution = pattern.findall(response.text)[0]
        
        if not lt:
            print('lt error')
        data = {
        'username': '13125195089',
        'password': '240011',
        'execution': execution,
        '_eventId': 'submit',
        'lt': lt,
        'verifyCode': '',
        'redirect': '',
        }
        return [scrapy.FormRequest(self.auth_url, formdata=data, callback=self.after_login)]
        
    def after_login(self, response):
        plate_urls = get_plate_urls(self.base_url)
        for plate_url in plate_urls:
            yield Request(plate_url, callback=self.parse_page)
    
    def parse_page(self, response):
        # 首先解析页面的每一个成交元素，yield item
        for li in response.xpath('//ul[@class="clinch-list"]/li'):
            deal_date, unit_price, total_price = li.xpath('.//div[@class="div-cun"]/text()').extract()
            print('成交日期：', deal_date)
            yield parser.chengjiao_sh(li)
        # 找到下一页的链接，若有，则生成新的Request    
        next_page_href = ''.join(response.css('a[gahref="results_next_page"]::attr(href)').re('/chengjiao/([0-9a-z]+/d[0-9]+)'))
        if not next_page_href:
            return
        next_page_url = self.base_url + next_page_href
        yield Request(next_page_url, callback=self.parse_page)
        
class XqSpider(Spider):
    #上海链家是个傻逼，会把重复的小区搞出来，所以爬下的数据有重复项。
    name = 'xq_sh'
    base_url = 'http://sh.lianjia.com/xiaoqu/'
    start_urls= get_plate_urls(base_url)
    allowed_domains = ['lianjia.com']
    def parse(self, response):
        for li in response.xpath('//ul[@id="house-lst"]/li'):
            item = parser.xiaoqu_sh(li)
            yield item
        # link to next page    
        next_page_href = ''.join(response.css('a[gahref="results_next_page"]::attr(href)').re('/xiaoqu/([0-9a-z]+/d[0-9]+)'))
        if not next_page_href:
            return
        next_page_url = self.base_url + next_page_href
        print(next_page_url)
        yield Request(next_page_url)
        
class PlateSpider(Spider):
    name = 'plate'
    base_url = 'http://sh.lianjia.com/xiaoqu/'
    start_urls=[base_url,]
    allowed_domains = ['lianjia.com']
    total = 0
    
    def parse(self, response):
        # start district requests
        districts = response.css('div[class="option-list gio_district"] a[gahref!="plate-nolimit"]::attr(href)').re('/xiaoqu/([0-9a-z]+?/)')
        for dis in districts:
            yield Request('http://sh.lianjia.com/xiaoqu/'+dis, callback=self.parse_plates)
            
    def parse_plates(self, response):
        # start plate requests
        num = response.xpath('/html/body/div[3]/div[2]/div[1]/h2/span/text()').extract()[0]
        self.total += int(num)
        print(self.total)
        '''
        plate_urls = response.css('div[class="option-list sub-option-list gio_plate"] a[gahref!="plate-nolimit"]::attr(href)').re('/xiaoqu/([0-9a-z]+?/)')
        plate_names = response.css('div[class="option-list sub-option-list gio_plate"] a[gahref!="plate-nolimit"]::text').extract()
        for url, name in zip(plate_urls, plate_names):
            yield Plate(name=name, url=url)'''
            
