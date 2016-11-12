from lianjia.items import Chengjiao, Xiaoqu
import re

def ershoufang_sh(li):
    mid = li.xpath('.//a[@name="selectDetail"]/@key').extract()[0]
    title = li.css('div[class="info-panel"] > h2 > a::text ').extract()[0]
    
    where = li.xpath('.//div[@class="where"]')
    xq_name = where.xpath('./a/span[@class="nameEllipsis"]/text()').extract()[0]
    house_type = where.xpath('./span[1]/text()').extract()[0].strip()
    size = where.xpath('./span[2]/text()').re('[0-9\.]+')[0]
    
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
                built_year = re.search('[0-9]+', con).group()
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
    unit_price = li.css('div[class="price-pre"]::text').re('[0-9]+')[0]
    visited = li.css('div[class="square"] > div > span::text').extract()[0]

def chengjiao_sh(li):
    mid = li.css('h2[class="clear"] > a::attr(key)').extract()[0]
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
    item = Chengjiao(mid=mid, xq_name=xq_name, house_type=house_type, size=size, storey=storey, orientation=orientation,
                    decoration=decoration, five_year=five_year, two_year=two_year, subway=subway, deal_date=deal_date,
                    unit_price=unit_price, total_price=total_price)
    return item
    
def xiaoqu_sh(li):
    item = Xiaoqu()

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