from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from lianjia.items import Chengjiao, Xiaoqu, Ershoufang, Plate
from scrapy.conf import settings
import lianjia.parsers as parser
import scrapy, re, json

CITY_TAGS = settings['CITY_TAGS']

def get_plate_urls(base_url, city):
    urls = []
    try:
        with open('./plates/%s.dat' %city, 'r') as f:
            for line in f.readlines():
                urls.append(base_url + json.loads(line)['url'])
    except FileNotFoundError:
    # 说明没有下载城市地区数据
        print('请先使用plate下载%s的地区数据' % CITY_TAGS[city])
        return
    return urls
'''
def get_zf_esf_urls(city):
    # 从数据库获取该城市的所有小区ID并生成zf和esf的链接
    conn = sqlite3.connect(settings['DB_NAME'])
    conn.text_factory = str
    cursor = conn.cursor()
    sql = 'SELECT 小区ID FROM XIAOQU WHERE 所在城市 = "%s"' % CITY_TAGS[city]
    cursor.execute(sql)
    res = cursor.fetchall()
    conn.close()
    return list(map(lambda x:list(x)[0], res))'''

class PlateSpider(Spider):
    # 使用LianjiaSpider之前要使用这个下载所有的区域列表
    name = 'plate'
    allowed_domains = ['lianjia.com']
    def __init__(self, city, *args, **kwargs):
        super(PlateSpider, self).__init__(*args, **kwargs)
        self.city = city
        self.start_urls = ['http://%s.lianjia.com/xiaoqu/' % city]
        
    def parse(self, response):
        districts = response.xpath('.//div[@data-role="ershoufang"]/div[1]/a/@href').re('/xiaoqu/(.*?/)')
        for district in districts:
            yield Request(self.start_urls[0]+district, callback=self.parse_plates)
    
    def parse_plates(self, response):
        plate_names = response.xpath('.//div[@data-role="ershoufang"]/div[2]/a/text()').extract()
        plate_urls = response.xpath('.//div[@data-role="ershoufang"]/div[2]/a/@href').re('/xiaoqu/(.*?/)')
        for plate_name, plate_url in zip(plate_names, plate_urls):
            yield Plate(name=plate_name, url=plate_url) 

class LianjiaSpider(CrawlSpider):
    name = 'lj'
    allowed_domains = ['lianjia.com']
    rules = (
        Rule(LinkExtractor(allow=('chengjiao/c',), restrict_xpaths=('//li[@class="clear xiaoquListItem"]',)), follow=False, callback='parse_chengjiao'),
        Rule(LinkExtractor(allow=('zufang/c'), restrict_xpaths=('//li[@class="clear xiaoquListItem"]',)), follow=False, callback='parse_zufang'),
        Rule(LinkExtractor(allow=('ershoufang/c'), restrict_xpaths=('//li[@class="clear xiaoquListItem"]',)), follow=False, callback='parse_ershoufang')
    )
    
    def __init__(self, city='bj', *args, **kwargs):
        super(LianjiaSpider, self).__init__(*args, **kwargs)
        self.city = city
        self.start_urls = []
        self.start_urls = get_plate_urls('http://%s.lianjia.com/xiaoqu/' % city, city)
    
    def get_page_num(self, response):
        try:
            total_page_num = response.xpath('.//div[@class="page-box house-lst-page-box"]/@page-data').extract()[0]
        except IndexError:
        # 这地方网页可能会抽风，本来有数据的返回的没有数据
            return 0, 0
        d = eval(total_page_num)
        total_page_num = d.get('totalPage')
        current_page = d.get('curPage')
        return total_page_num, current_page
            
    def parse_start_url(self, response):
        for li in response.xpath('.//li[@class="clear xiaoquListItem"]'):
            yield parser.xiaoqu(li, self.city)
            
        total_page_num, current_page = self.get_page_num(response)
        if current_page != 1:
            return
        else:
            for page_num in range(2, total_page_num+1):
                yield Request(response.url+'pg%d/' % page_num)
                
    def parse_chengjiao(self, response): 
        xq_id = re.search('[0-9]+', response.url).group()
        for li in response.xpath('//div[@class="leftContent"]/ul[@class="listContent"]/li'):
            yield parser.chengjiao(li, xq_id)
        
        total_page_num, current_page = self.get_page_num(response)
        if current_page != 1:
            return
        else:
            for page_num in range(2, total_page_num+1):
                yield Request(response.url+'pg%d/' % page_num, self.parse_chengjiao)
        
    def parse_zufang(self, response):
        xq_id = re.search('[0-9]+', response.url).group()
        for li in response.xpath('//div[@class="main-box clear"]//ul[@id="house-lst"]/li'):
            yield parser.zufang(li, xq_id)
        
        total_page_num, current_page = self.get_page_num(response)
        if current_page != 1:
            return
        else:
            for page_num in range(2, total_page_num+1):
                yield Request(response.url+'pg%d/' % page_num, self.parse_zufang)
                
    def parse_ershoufang(self, response):
        xq_id = re.search('[0-9]+', response.url).group()
        for li in response.xpath('//div[@class="leftContent"]/ul[@class="sellListContent"]/li'):
            yield parser.ershoufang(li, xq_id)
        
        total_page_num, current_page = self.get_page_num(response)
        if current_page != 1:
            return
        else:
            for page_num in range(2, total_page_num+1):
                yield Request(response.url+'pg%d/' % page_num, self.parse_ershoufang)
            
class UpdateSpider(CrawlSpider):
    # 以小区为基本单位进行更新，阉割版的LianjiaSpider
    name = 'lj_up'
    allowed_domains = ['lianjia.com']
    rules = (
        Rule(LinkExtractor(allow=('zufang/c'), restrict_xpaths=('//li[@class="clear xiaoquListItem"]',)), follow=False, callback='parse_zufang'),
        Rule(LinkExtractor(allow=('ershoufang/c'), restrict_xpaths=('//li[@class="clear xiaoquListItem"]',)), follow=False, callback='parse_ershoufang')
    )
    
    def __init__(self, city='bj', *args, **kwargs):
        super(UpdateSpider, self).__init__(*args, **kwargs)
        self.start_urls = []
        self.start_urls = get_plate_urls('http://%s.lianjia.com/xiaoqu/' % city, city)
    
    def get_page_num(self, response):
        try:
            total_page_num = response.xpath('.//div[@class="page-box house-lst-page-box"]/@page-data').extract()[0]
        except IndexError:
        # 这地方网页可能会抽风，本来有数据的返回的没有数据
            return 0, 0
        d = eval(total_page_num)
        total_page_num = d.get('totalPage')
        current_page = d.get('curPage')
        return total_page_num, current_page
            
    def parse_start_url(self, response):
        '''
        for li in response.xpath('.//li[@class="clear xiaoquListItem"]'):
            yield parser.xiaoqu(li, self.city)'''
        total_page_num, current_page = self.get_page_num(response)
        if current_page != 1:
            return
        else:
            for page_num in range(2, total_page_num+1):
                yield Request(response.url+'pg%d/' % page_num)
        
    def parse_zufang(self, response):
        xq_id = re.search('[0-9]+', response.url).group()
        for li in response.xpath('//div[@class="main-box clear"]//ul[@id="house-lst"]/li'):
            yield parser.zufang(li, xq_id)
        
        total_page_num, current_page = self.get_page_num(response)
        if current_page != 1:
            return
        else:
            for page_num in range(2, total_page_num+1):
                yield Request(response.url+'pg%d/' % page_num, self.parse_zufang)
                
    def parse_ershoufang(self, response):
        xq_id = re.search('[0-9]+', response.url).group()
        for li in response.xpath('//div[@class="leftContent"]/ul[@class="sellListContent"]/li'):
            yield parser.ershoufang(li, xq_id)
        
        total_page_num, current_page = self.get_page_num(response)
        if current_page != 1:
            return
        else:
            for page_num in range(2, total_page_num+1):
                yield Request(response.url+'pg%d/' % page_num, self.parse_ershoufang)