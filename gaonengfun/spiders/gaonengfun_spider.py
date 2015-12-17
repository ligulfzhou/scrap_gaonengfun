import scrapy
from gaonengfun.items import GaonengfunItem

class GaonengfunSpider(scrapy.Spider):
    name = "gaonengfun"
    allowed_domains = ["gaonengfun.com"]
    start_urls = [
        "http://www.gaonengfun.com/show/%s" % x for x in xrange(100000, 200000)
    ]

    #title: /html/body/div[2]/div/div/div[1]/div/div/div[1]
    #content: /html/body/div[2]/div/div/div[2]/div/p
    def parse(self, respose):
        for sel in response.xpath('/html/body/div[2]/div/div/'):
            title = sel.xpath('div[1]/div/div/div[1]/text()').extract()
            if not title:
                return
            item = GaonengfunItem()
            item['title'] = title

            item['content'] = ""
            item['imgs'] = []
            for p in response.xpath('/div[2]/div/p'):
                a = p.xpath('a/@href/text()').extract()
                if not a:
                    item['content'].join(p.extract())
                else:
                    item['content'].join(" " + a.split('/')[-1] + " ")
                    item['imgs'].append(a.split('/'[-1]))
            yield item
