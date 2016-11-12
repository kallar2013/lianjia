from lianjia.items import Chengjiao, Xiaoqu
import re



def chengjiao_sh(li):
    mid = li.css('h2[class="clear"] > a::attr(key)').extract()[0]
    xq_name, house_type, size = li.css('h2[class="clear"] > a::text').extract()[0].split(' ', 2)
    size = float(re.search('[0-9.]+', size).group())

    cons = li.xpath('./div[2]/div[1]/div[1]/div/text()').re('[^\t\n\r\s]+')
    def filt(con, x):
        if con.find(x) != -1:
            return con
        else:
            return ''
                
    if len(cons) == 3:
        storey, orientation, decoration = cons
    else:
        for con in cons:
            storey = filt(con, '层')
            orientation = filt(con, '朝')
            decoration = filt(con, '装')

    introduce = li.xpath('.//div[@class="introduce"]/span/text()').extract()
    five_year, two_year, subway = '', '', ''
    for span in list(map(lambda x:x.strip(), introduce)):
        five_year = filt(span, '满五')
        two_year = filt(span, '满二')
        subway = filt(span, '距离')
    deal_date, unit_price, total_price = li.xpath('.//div[@class="div-cun"]/text()').extract()
    item = Chengjiao(mid=mid, xq_name=xq_name, house_type=house_type, size=size, storey=storey, orientation=orientation,
                    decoration=decoration, five_year=five_year, two_year=two_year, subway=subway, deal_date=deal_date,
                    unit_price=unit_price, total_price=total_price)
    return item
    
def xiaoqu_sh(li, url):
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