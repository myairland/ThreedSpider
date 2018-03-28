
# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ThreedSpider.items import Bbs3drrrItem


class Bbs3drrrSpider(CrawlSpider):
    name = 'tieba'
    allowed_domains = ['tieba.baidu.com']
    start_urls = ['https://tieba.baidu.com/f?kw=3d%E6%89%93%E5%8D%B0&ie=utf-8&pn=0']

    rules = (
        Rule(LinkExtractor(allow='.*html', )),
    )

    itemIndex = 421

    pageNum = -1
    
    def parse(self, response):
        
        for a in response.css('a.j_th_tit'):
            yield response.follow(a,callback=self.parse_item)
        pass

        nextPage = response.css('a.next.pagination-item::attr(href)').extract_first()
        yield scrapy.Request("https:" + nextPage, callback=self.parse) 
        # if nextPage is not None:
        #     yield response.follow(a,callback=self.parse)
        # self.pageNum = self.pageNum + 1
        # self.pageNum = self.pageNum * 50
        # yield scrapy.Request("https://tieba.baidu.com/f?kw=3d%%E6%%89%%93%%E5%%8D%%B0&ie=utf-8&pn=%(num)s"%{'num':self.pageNum}, callback=self.parse)
        #if nextPage is not None:
        #    yield response.follow(nextPage,callback=self.parse_thread)

    def parse_item(self,response):
        #具体内容
        item = Bbs3drrrItem()
        item['title'] = response.css(".core_title_txt::text").extract_first()
        item['content'] = response.css(".d_post_content_firstfloor .j_d_post_content").extract_first()
        item['itemIndex'] = self.itemIndex
        self.itemIndex = self.itemIndex + 1
        yield item
