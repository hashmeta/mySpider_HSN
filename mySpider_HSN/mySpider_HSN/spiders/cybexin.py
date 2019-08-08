# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from mySpider_HSN.items import MyspiderHsnItem
class CybexinSpider(CrawlSpider):
    name = 'cybexin'
    allowed_domains = ['http://www.cybex.in']
    start_urls = ['http://www.cybex.in/indian-custom-duty/Live-Animals-Chapter-01.aspx']
    def __init__(self,filename=None):
        if filename:
            with open(filename, 'r') as f:
                for line in f:
                    self.start_urls.append(line.rstrip())
    def make_requests_from_url(self, url):
        return scrapy.Request(url, dont_filter=True, meta = {
                  'dont_redirect': True,
                  'handle_httpstatus_list': [301,302]
            })
    def parse(self, response):
        data=response.xpath('//tr[contains(@class,"GridView")]')
        for d in data[1:]:
            item=MyspiderHsnItem()
            item['HSN_Code']=d.xpath('td[1]/a/text()').extract_first()
            item['Desc']=d.xpath('td[2]/a/text()').extract_first()
            yield item
