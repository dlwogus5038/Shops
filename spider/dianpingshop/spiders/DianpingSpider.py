# coding=utf-8
# -*- coding : utf-8-*-

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from dianpingshop.items import DianpingItem
import time
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

#
class DianpingSpider(CrawlSpider):

    name = 'dianpingshop'

    start_urls=['http://www.dianping.com/search/category/2/10']

    location=['r2580','r1471','r2578','r1466','r1470','r1469','r2078','r1489','r1488','r2579','r2871','r1475','r1467','r1481','r1465','r2583']

    foodtype=['g110','g132','g508','g117','g113','g112','g111','g116','g311','g114','g101','g103','g102','g104',
'g108','g109','g3243','g26481','g115','g1783','g248','g105','g26483','g246','g106','g1845','g118','g251','g219','g1817','g1338','g250','g26482', 'g107']


    ## 爬取顺序:
    ## 1. 先爬取基础数据结构 location, foodtype  --> 独立
    ## 2. 根据基础数据组合出要爬取的 url , 即某一地区某菜系的所有商户页面
    ##    2.1  抓取这个页面有多少 分页 数据
    ##    2.2

    def parse_start_url(self, response):

        url = 'http://www.dianping.com/search/category/2/10'

        for lbs in self.location:

            for ft in self.foodtype:
                url = 'http://www.dianping.com/search/category/2/10/%s%s' % (lbs, ft)

                yield Request(url,callback=self.parse_list_first)

    def parse_list(self, response):

        #item = DianpingItem()

        selector = Selector(response)

        div = selector.xpath('//div[@id="shop-all-list"]/ul/li')


        for dd in div:
            shopurls = dd.xpath('div[2]/div[1]/a[1]/@href').extract()
            info_url = 'http://www.dianping.com'+str(shopurls[0])
            #print info_url
            yield Request(info_url, callback=self.parse_info)

    def parse_info(self,response):
        print('Here is response!!')
        print response
        item = DianpingItem()
        selector = Selector(response)

        div = selector.xpath('//div[@id="basic-info"]')
        short_div = selector.xpath('//div[@class="breadcrumb"]')

        pic = selector.xpath('//a[@class="J_main-photo"]/img/@src').extract_first()
        item['pic'] = pic

        foodtype = short_div.xpath('a[3]/text()').extract_first()
        temp = foodtype[13:]
        item['foodtype'] = temp[:-9]

        loc = short_div.xpath('a[2]/text()').extract_first()
        temp = loc[13:]
        item['loc'] = temp[:-9]

        shopname = div.xpath('h1/text()').extract_first()
        temp = shopname[1:]
        item['shopname'] = temp[:-1]
        print shopname

        shopurl = response.url
        item['shopurl'] = shopurl

        item['ID'] = shopurl[29:]

        shoplevelstr = div.xpath('div[1]/span[1]/@class').extract_first()
        shoplevel = shoplevelstr[-2] + '.' + shoplevelstr[-1]
        item['shoplevel'] = shoplevel

        avgcost = div.xpath('div[1]/span[3]/text()').extract_first()
        item['avgcost'] = avgcost

        taste = div.xpath('div[1]/span[4]/span[1]/text()').extract_first()
        item['taste'] = taste[3:]

        envi = div.xpath('div[1]/span[4]/span[2]/text()').extract_first()
        item['envi'] = envi[3:]

        service = div.xpath('div[1]/span[4]/span[3]/text()').extract_first()
        item['service'] = service[3:]

        street_address = div.xpath('div[2]/span[2]/@title').extract_first()
        item['street_address'] = street_address

        tel = div.xpath('p/span[2]/text()').extract_first()
        item['tel'] = tel

        div_comments = selector.xpath('//ul[@class="comment-list J-list"]/li')
        comments = []
        for comment in div_comments:
            flag = comment.xpath('div/div/@class').extract_first()
            if flag == 'photos':
                context = comment.xpath('div/p[2]/text()').extract_first()
                if context != '':
                    print context
                    comments.append(context)
            elif flag == 'info J-info-short':
                context = comment.xpath('div/div[2]/p/text()').extract_first()
                if context != '':
                    print context
                    comments.append(context)
        item['comments'] = comments

        yield item




    def parse_list_first(self, response):

        selector = Selector(response)


        #########################################
        #### 获取分页

        pg = 0

        pages = selector.xpath('//div[@class="page"]/a/@data-ga-page').extract()

        if len(pages) > 0:
            pg = pages[len(pages) - 2]


        pg=int(str(pg))+1



        url = str(response.url)

        for p in range(1,pg):
            ul = url+'p'+str(p)

            yield Request(ul,callback=self.parse_list)
