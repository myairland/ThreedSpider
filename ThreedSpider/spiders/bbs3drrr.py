# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ThreedSpider.items import Bbs3drrrItem


class Bbs3drrrSpider(CrawlSpider):
    name = 'bbs3drrr'
    allowed_domains = ['bbs.3drrr.com']
    start_urls = ['http://bbs.3drrr.com/forum-57-1.html']

    rules = (
        Rule(LinkExtractor(allow='.*html', )),
    )

    itemIndex = 426
    
    def parse(self, response):
        
        for a in response.css('a.s.xst'):
            yield response.follow(a,callback=self.parse_item)
        pass

        nextPage = response.css('a.nxt::attr(href)').extract_first()
        if nextPage is not None:
            yield scrapy.Request(nextPage, callback=self.parse)
        #if nextPage is not None:
        #    yield response.follow(nextPage,callback=self.parse_thread)

    def parse_item(self,response):
        #具体内容
        item = Bbs3drrrItem()
        item['title'] = response.css("#thread_subject::text").extract_first()
        item['content'] = response.css(".t_f").extract_first()
        item['itemIndex'] = self.itemIndex
        self.itemIndex = self.itemIndex + 1
        yield item
