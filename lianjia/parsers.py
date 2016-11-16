from lianjia.items import Chengjiao_sh, Xiaoqu_sh, Ershoufang_sh, Chengjiao, Xiaoqu, Ershoufang, Zufang
import re
import datetime
from scrapy.conf import settings

CITY_TAGS = settings['CITY_TAGS']
crawl_date = str(settings['DATE'])

def xiaoqu(li, city):
    # 一般我们不会得到空的搜索结果，当在搜索小区的时候
    '''
    mid = scrapy.Field()
    name = scrapy.Field()
    #house_type_num = scrapy.Field()
    thirty_days = scrapy.Field()
    #ninety_days = scrapy.Field()
    onrent = scrapy.Field()
    mtype = scrapy.Field()
    built_year = scrapy.Field()
    subway = scrapy.Field()
    #school = scrapy.Field()
    price = scrapy.Field()
    onsale = scrapy.Field()
    plate = scrapy.Field()
    district = scrapy.Field()
    city = scrapy.Field()'''
    
    mid = li.xpath('.//div[@class="title"]/a/@href').re('/xiaoqu/(.+?)/')[0]
    name = li.xpath('.//div[@class="title"]/a/text()').extract()[0]
    houseInfos = li.xpath('.//div[@class="houseInfo"]/a')
    for houseInfo in houseInfos:
        if '户型' in houseInfo.xpath('./text()').extract()[0]:
            continue
        elif '成交' in houseInfo.xpath('./text()').extract()[0]:
            pattern = re.compile('成交(\d)+套')
            deals = houseInfo.xpath('./text()').extract()[0]
            if '30天' in deals:
                thirty_days = pattern.findall(deals)[0]; ninety_days = ''
            elif '90天' in deals:
                ninety_days = pattern.findall(deals)[0]; thirty_days = ''
        elif '出租' in houseInfo.xpath('./text()').extract()[0]:
            onrent = int(houseInfo.xpath('./text()').re('([0-9]+)套')[0])
    positionInfo = li.xpath('.//div[@class="positionInfo"]/text()').re('[\S]+')
    mtype = positionInfo[0]
    if len(positionInfo) == 3:
        built_year = re.search('[0-9]+', positionInfo[2])
    else:
        built_year = re.search('[0-9]+', positionInfo[1])
    if built_year:
        built_year = built_year.group()
    else:
        built_year = ''
    subway = ''.join(li.xpath('.//div[@class="tagList"]/span/text()').extract())
    price = li.xpath('.//div[@class="totalPrice"]/span/text()').extract()[0]
    if '暂无' not in price:
        price = int(price)
    else:
        price = 0
    onsale = int(li.xpath('.//div[@class="xiaoquListItemSellCount"]/a/span/text()').extract()[0])
    district = li.xpath('.//a[@class="district"]/text()').extract()[0]
    plate = li.xpath('.//a[@class="bizcircle"]/text()').extract()[0]
    city = CITY_TAGS[city]
    return Xiaoqu(mid=mid, name=name, thirty_days=thirty_days, ninety_days=ninety_days, onrent=onrent, mtype=mtype, built_year=built_year, 
        subway=subway, price=price, onsale=onsale, district=district, plate=plate, city=city)

def chengjiao(li, xq_id):
    '''
    mid = scrapy.Field()
    xq_name = scrapy.Field()
    #xq_id = scrapy.Field()
    house_type = scrapy.Field()
    size = scrapy.Field()
    storey = scrapy.Field()
    orientation = scrapy.Field()
    mtype = scrapy.Field()
    built_year = scrapy.Field()
    decoration = scrapy.Field()
    subway = scrapy.Field()
    #school = scrapy.Field()
    five_year = scrapy.Field()
    two_year = scrapy.Field()
    elevator = scrapy.Field()
    deal_date = scrapy.Field()
    unit_price = scrapy.Field()
    total_price = scrapy.Field()'''
    
    info = li.css('div[class="title"]')
    mid = ''.join(info.css('a::attr(href)').re('chengjiao/(.+?)\.'))
    try:
        xq_name, house_type, size = info.css('a::text').extract()[0].split()
    except IndexError:
        xq_name, house_type, size = info.xpath('./text()').extract()[0].split()
        
    size = int(re.search('[0-9]+', size).group())
    
    orientation, decoration, elevator = li.css('div[class="houseInfo"]::text').extract()[0].replace(' ', '').replace('\xa0', '').split('|')
    storey, built_year = li.css('div[class="positionInfo"]::text').extract()[0].split(' ')
    if built_year:
        try:
            built_year, mtype = built_year.split('年建', 1)
        except ValueError:
            built_year = ''
            mtype = built_year
    else:
        mtype = ''
    
    tags = li.css('span[class="dealHouseTxt"] span::text').extract()
    two_year, subway, five_year = ['']*3
    for tag in tags:
        if '两年' in tag:
            two_year = tag
        elif '距' in tag:
            subway = tag
        elif '五年' in tag:
            five_year = tag
    deal_date = li.css('div[class="dealDate"]::text').extract()[0].replace('.', '-')
    try:
        total_price = li.css('div[class="totalPrice"] > span::text').extract()[0]
    except IndexError:
        total_price = 0
    try:
        unit_price = li.css('div[class="unitPrice"] > span::text').extract()[0]
    except IndexError:
        unit_price = 0
    return Chengjiao(mid=mid, xq_id=xq_id, xq_name=xq_name, size=size, house_type=house_type, orientation=orientation,
            decoration=decoration, elevator=elevator, storey=storey, built_year=built_year, mtype=mtype, subway=subway,
            two_year=two_year, five_year=five_year, deal_date=deal_date, total_price=total_price, unit_price=unit_price)

def zufang(li, xq_id):
    '''
    mid = scrapy.Field()
    title = scrapy.Field()
    #xq_id = scrapy.Field()
    house_type = scrapy.Field()
    size = scrapy.Field()
    orientation = scrapy.Field()
    storey = scrapy.Field()
    built_year = scrapy.Field()
    mtype = scrapy.Field()
    visited = scrapy.Field()
    last_updated = scrapy.Field()
    subway = scrapy.Field()
    heat = scrapy.Field()
    decoration = scrapy.Field()
    balcony = scrapy.Field()
    only = scrapy.Field()
    rent = scrapy.Field()
    other_tags = scrapy.Field()
    #crawl_date = scrapy.Field()'''
    
    info = li.css('div[class="info-panel"] > h2')
    mid = info.css('a::attr(href)').re('zufang/(.+?)\.html')[0]
    title = info.css('a::attr(title)').extract()[0]
    house_type, size, orientation = list(map(lambda x:x.strip(), li.css('div[class="where"] > span ::text').extract()))
    size = int(re.search('[0-9]+', size).group())
    con = li.css('div[class="con"]::text').extract()
    if len(con) == 2:
        storey, built_year = con
    elif '楼' in con:
        storey = con; built_year = ''
    elif '年' in con:
        buil_year = con; storey = ''
    else:
        built_year, storey = '', ''
    if '年建' in built_year and ('楼' in built_year or '结合' in built_year):
        built_year, mtype = built_year.split('年建', 1)
    elif '年建' not in built_year:
        built_year = ''; mtype = built_year
    else:
        mtype = ''
    rent = int(li.css('div[class="price"] > span::text').extract()[0])
    last_updated = li.css('div[class="price"]+div::text').re('[0-9\.]+')[0].replace('.', '-')
    visited = int(li.css('div[class="square"]>div>span::text').extract()[0])
    
    tags = li.css('div[class="view-label left"] span::text').extract()
    subway, decoration, heat, balcony, only = [0]*5
    other_tags = []
    for tag in tags:
        if '距离' in tag:
            subway = 1
        elif '装' in tag:
            decoration = 1
        elif '暖' in tag:
            heat = 1
        elif '阳台' in tag:
            balcony = 1
        elif '独家' in tag:
            only = 1
        else:
            other_tags.append(tag)
            continue
    other_tags = '/'.join(other_tags)
    
    return Zufang(mid=mid, title=title, xq_id=xq_id, house_type=house_type, size=size, orientation=orientation, 
            storey=storey, built_year=built_year, mtype=mtype, visited=visited, last_updated=last_updated, subway=subway,
            heat=heat, decoration=decoration, balcony=balcony, only=only, rent=rent, other_tags=other_tags, crawl_date=crawl_date)

def ershoufang(li, xq_id):
    '''
    mid = scrapy.Field()
    title = scrapy.Field()
    #xq_id = scrapy.Field()
    house_type = scrapy.Field()
    size = scrapy.Field()
    orientation = scrapy.Field()
    decoration = scrapy.Field()
    elevator = scrapy.Field()
    storey = scrapy.Field()
    built_year = scrapy.Field()
    mtype = scrapy.Field()
    focus = scrapy.Field()
    visited = scrapy.Field()
    publish_date = scrapy.Field()
    five_year = scrapy.Field()
    two_year = scrapy.Field()
    #school = scrapy.Field()
    subway = scrapy.Field()
    total_price = scrapy.Field()
    unit_price = scrapy.Field()
    #crawl_date = scrapy.Field()'''
    
    mid = li.css('div[class="title"]>a::attr(href)').re('ershoufang/(.+?)\.')[0]
    title = li.css('div[class="title"]>a::text').extract()[0]
    houseInfo = li.css('div[class="houseInfo"]::text').extract()[0].replace(' ', '').split('|')[1:]
    if len(houseInfo) == 5:
        house_type, size, orientation, decoration, elevator = houseInfo
    else:
        house_type, size, orientation, decoration = houseInfo
        elevator = ''
    
    size = float(re.search('[0-9\.]+', size).group())
    elevator = int('有' in elevator)
    
    storey, built_year = li.css('div[class="positionInfo"]::text').re('[\S]+')[:2]
    if '年建' in built_year and ('楼' in built_year or '结合' in built_year):
        built_year, mtype = built_year.split('年建', 1)
    elif '年建' not in built_year:
        built_year = ''; mtype = built_year
    else:
        built_year = re.search('[0-9]+', built_year).group(); mtype = ''
        
    focus, visited, publish_date = li.css('div[class="followInfo"]::text').extract()[0].replace(' ', '').split('/')
    focus = int(re.search('[0-9]+', focus).group())
    visited = int(re.search('[0-9]+', visited).group())
    if '天' in publish_date:
        publish_date = str(settings['DATE'] - datetime.timedelta(days=int(re.search('[0-9]+', publish_date).group())))
    elif '月' in publish_date:
        publish_date = str(settings['DATE'] - datetime.timedelta(weeks=(int(re.search('[0-9]+', publish_date).group()))*4))
    
    tags = li.css('div[class="tag"]>span::text').extract()
    subway, five_year, two_year = ['']*3
    for tag in tags:
        if '距离' in tag:
            subway = tag
        elif '两年' in tag:
            two_year = tag
        elif '五年' in tag:
            five_year = tag
    total_price = li.css('div[class="totalPrice"]>span::text').extract()[0]
    unit_price = li.css('div[class="unitPrice"]::attr(data-price)').extract()[0]
    if '暂无' not in total_price:
        total_price = float(total_price)
    else:
        total_price = 0
    if '暂无' not in unit_price:
        unit_price = int(unit_price)
    else:
        unit_price = 0
    return Ershoufang(mid=mid, title=title, xq_id=xq_id, house_type=house_type, size=size, orientation=orientation,
        decoration=decoration, elevator=elevator, storey=storey, built_year=built_year, mtype=mtype, focus=focus,
        visited=visited, publish_date=publish_date, five_year=five_year, two_year=two_year, subway=subway, 
        total_price=total_price, unit_price=unit_price, crawl_date=crawl_date)

def ershoufang_sh(li):
    try:
        mid = li.xpath('.//a[@name="selectDetail"]/@key').extract()[0]
    except IndexError:
        return
    title = li.css('div[class="info-panel"] > h2 > a::text ').extract()[0]
    
    where = li.xpath('.//div[@class="where"]')
    xq_id = where.xpath('./a[@class="laisuzhou"]/@href').re('/([0-9]+)\.')[0]
    xq_name = where.xpath('./a/span[@class="nameEllipsis"]/text()').extract()[0]
    house_type = where.xpath('./span[1]/text()').extract()[0].strip()
    size = float(where.xpath('./span[2]/text()').re('[0-9\.]+')[0])
    
    cons = li.xpath('./div[2]/div[1]/div[2]/div/text()').re('[^\s\n\t\r]+')
    storey, orientation, built_year = ['']*3
    if len(cons) == 3:
        storey, orientation, built_year = cons
    else:
        for con in cons:
            if '层' in con:
                storey = con
            elif '朝' in con:
                orientation = con
            elif '建' in con:
                built_year = con
    if built_year:
        built_year = re.search('[0-9]+', built_year).group()
    labels = li.xpath('.//div[@class="view-label left"]//text()').re('[^\s\t\r\n]+')
    
    subway, five_year, two_year, haskey = ['']*4
    for label in labels:
        if '距' in label:
            subway = label
        elif '满五' in label:
            five_year = label
        elif '满二' in label:
            two_year = label
        elif '钥匙' in label:
            haskey = label
            
    total_price = li.css('div[class="price"] > span::text').extract()[0]
    if '暂无' not in total_price:
        total_price = float(total_price)
    else:
        total_price = 0
    unit_price = li.css('div[class="price-pre"]::text').re('[0-9]+')[0]
    if '暂无' not in unit_price:
        unit_price = int(unit_price)
    else:
        unit_price = 0
    visited = int(li.css('div[class="square"] > div > span::text').extract()[0])
    
    item = Ershoufang_sh(mid=mid, xq_id=xq_id, title=title, house_type=house_type, built_year=built_year, size=size,
        orientation=orientation, storey=storey, visited=visited, five_year=five_year, two_year=two_year, haskey=haskey,
        subway=subway, total_price=total_price, unit_price=unit_price, crawl_date=crawl_date)
    return item

def chengjiao_sh(li):
    try:
        mid = li.css('h2[class="clear"] > a::attr(key)').extract()[0]
    except IndexError:
        return
    xq_name, house_type, size = li.css('h2[class="clear"] > a::text').extract()[0].split(' ', 2)
    size = float(re.search('[0-9.]+', size).group())

    cons = li.xpath('./div[2]/div[1]/div[1]/div/text()').re('[^\t\n\r\s]+')

    storey, orientation, decoration = ['']*3       
    if len(cons) == 3:
        storey, orientation, decoration = cons
    else:
        for con in cons:
            if '层' in con:
                storey = con
            elif '朝' in con:
                orientation = con
            elif '装' in con:
                decoration = con

    introduce = li.xpath('.//div[@class="introduce"]/span/text()').extract()
    five_year, two_year, subway = ['']*3
    for span in list(map(lambda x:x.strip(), introduce)):
        if '满五' in span:
            five_year = span
        elif '满二' in span:
            two_year = span
        elif '距离' in span:
            subway = span
            
    deal_date, unit_price, total_price = li.xpath('.//div[@class="div-cun"]/text()').extract()
    return Chengjiao_sh(mid=mid, xq_name=xq_name, house_type=house_type, size=size, storey=storey, orientation=orientation,
            decoration=decoration, five_year=five_year, two_year=two_year, subway=subway, deal_date=deal_date,
            unit_price=unit_price, total_price=total_price)
    
def xiaoqu_sh(li):
    item = Xiaoqu_sh()

    item['mid'] = li.xpath('.//a[@name="selectDetail"]/@key').extract()[0]

    where = li.xpath('.//a[@class="actshowMap_list"]')
    coordinate = where.xpath('@xiaoqu').extract()[0].lstrip('[').rstrip(']').replace(' ', '')
    x, y, title = coordinate.split(',', 2)
    title = title.strip("'")
    item['title'] = title
    item['coordinate'] = str(x) + ',' + str(y)

    item['district'] = where.xpath('@districtname').extract()[0]
    item['platename'] = where.xpath('@platename').extract()[0]


    item['year'] = li.xpath('.//div[@class="con"]/text()').re('[0-9]+')[0]

    tag = ''.join(li.xpath('.//span[@class="fang-subway-ex"]/span/text()').re('(\S+)'))
    item['ditie'] = tag

    item['city'] = '上海'

    price = li.xpath('.//div[@class="price"]/span/text()').re('[\S]+')[0]
    if price.find('暂无') != -1:
        price = 0
    else:
        price = int(price)
    item['price'] = price

    onsale = li.xpath('.//div[@class="square"]/div/a/span/text()').extract()[0]
    item['onsale'] = int(onsale)
    return item