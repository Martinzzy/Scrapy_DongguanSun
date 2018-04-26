# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from datetime import datetime
from ..items import DongguanSunItemLoader,DongguanSunItem

class SunSpider(scrapy.Spider):
    name = 'sun'
    allowed_domains = ['wz.sun0769.com/index.php/question/report?page=0']
    start_urls = ['http://wz.sun0769.com/index.php/question/report?page=0']

    custom_settings = {'DOWNLOAD_DELAY':2,
                       'COOKIES_ENABLED':False,
                       'DEFAULT_REQUEST_HEADERS':
                           {
                           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
                       }
                    }

    def parse(self, response):
        selector = response.xpath('//td[@align="center"]//tr')
        for sel in selector:
            question_url = sel.xpath('./td[2]/a[2]/@href').extract_first()
            yield Request(url=question_url,callback=self.parse_question,dont_filter=True,)


        next_page = response.xpath('//div[@class="pagination"]/a[last()-1]/@href').extract_first()
        if next_page:
            yield Request(url=next_page,callback=self.parse,dont_filter=True)


    def parse_question(self,response):

        item_loader = DongguanSunItemLoader(item=DongguanSunItem(),response=response)

        item_loader.add_value("url",response.url)
        item_loader.add_xpath("title",'//div[@class="pagecenter p3"]//strong/text()')
        item_loader.add_xpath("id",'//div[@class="pagecenter p3"]//strong/text()')
        item_loader.add_css("content", "div.c1.text14_2::text")
        item_loader.add_css("status",".qgrn::text")
        item_loader.add_value("crawl_time",datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        question = item_loader.load_item()

        yield question