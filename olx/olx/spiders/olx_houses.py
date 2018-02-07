# -*- coding: utf-8 -*-
import scrapy
import datetime

today = datetime.date.today().strftime('%Y-%m-%d')

class OlxHousesSpider(scrapy.Spider):
    name = 'olx_houses'
    allowed_domains = ['olx.ro']
    start_urls = ['https://www.olx.ro/imobiliare/case-de-vanzare/oradea/',
    'https://www.olx.ro/imobiliare/apartamente-garsoniere-de-vanzare/oradea/',
    'https://www.olx.ro/imobiliare/apartamente-garsoniere-de-inchiriat/oradea/',
    'https://www.olx.ro/imobiliare/case-de-inchiriat/oradea/']

    download_delay=0.05

    def parse(self, response):
        for href in response.css('a.detailsLink::attr(href)'):
            yield response.follow(href, self.parse_details)
        for href in  response.css('a.pageNextPrev::attr(href)')[-1:]:
            yield response.follow(href, self.parse)

    def parse_details(self, response):
        tip = response.css("#breadcrumbTop .middle > ul > li:last-child > a::attr(title)").extract_first()  
        price = response.css('.price-label > strong::text').extract_first().replace(" ", "")
        attrs = {'url': response.url, 'text': response.css('#textContent>p::text').extract_first().strip(),
                'title':  response.css('h1::text').extract_first().strip(),
		'price': price,  'type': tip, 'date': today, 
                'nr_anunt':  response.css('.offer-titlebox em small::text').re('\d+'), 
                'adaugat_la': response.css('.offer-titlebox em::text').re('Adaugat (de pe telefon) +La (.*),') }
        for tr in response.css('.details').xpath('tr/td//tr'):
            title = tr.css('th::text').extract_first()
            value = " ".join(x.strip() for x in tr.xpath('td/strong//text()').extract() if x.strip()!="")
            attrs[title]=value
        yield attrs
 
