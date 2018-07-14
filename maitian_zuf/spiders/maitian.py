# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from ..items import MaitianZufItem, MaitianEsItem

def replace(s):
    pattern = re.compile(r'\r\n|\n|&nbsp;|\\xa0|\\u3000|\xa0')
    s = re.sub(pattern, '', s)
    return s.strip()

class MaitianSpider(scrapy.Spider):
    name = 'maitian'
    allowed_domains = ['bj.maitian.cn']
    start_urls = ['http://bj.maitian.cn/zfall', 'http://bj.maitian.cn/esfall']

    ua = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    custom_settings = {
        'CONCURRENT_REQUESTS': 64,
        'DOWNLOAD_DELAY': 0,
        'COOKIES_ENABLED': False,
        # 'LOG_LEVEL': 'INFO',
        'RETRY_TIMES': 15,
        'DEFAULT_REQUEST_HEADERS': {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
        },
        'MONGO_URI': 'localhost:27017',
        'MONGO_DATABASE': 'maitian',
        'PROXY_URL': 'http://localhost:5555/random',
        'ITEM_PIPELINES': {
            'maitian_zuf.pipelines.MongoPipeline': 301,
        },
        'DOWNLOADER_MIDDLEWARES': {
            # 'maitian_zuf.middlewares.ProxyMiddleware': 543,
        },
    }

    def parse(self, response):
        zf_url = response.url
        es_url = response.url

        # 租房
        if response.url == zf_url:
            for each in response.xpath('/html/body/section[2]/div[2]/div[2]/ul/li'):
                url = each.xpath('a/@href').extract_first().split('/')
                det_url = '/{}/{}'.format(url[-2], url[-1])
                # print(response.urljoin(det_url))
                yield Request(url=response.urljoin(det_url), callback=self.parse_zf,
                              headers={'User-Agent': self.ua, 'Referer': response.url},
                              meta={'zf_url': response.urljoin(det_url)})

            zf_next_page = response.xpath('//*[@id="paging"]/a[last()-1]/@href').extract_first()
            if zf_next_page is not None:
                zf_next_page = response.urljoin(zf_next_page)
                yield Request(url=zf_next_page, callback=self.parse,
                              headers={'User-Agent': self.ua, 'Referer': response.url})

        # 二手房
        if response.url == es_url:
            for each in response.xpath('/html/body/section[2]/div[2]/div[2]/ul/li'):
                url = each.xpath('a/@href').extract_first().split('/')
                det_url = '/{}/{}'.format(url[-2], url[-1])
                # print(response.urljoin(det_url))
                yield Request(url=response.urljoin(det_url), callback=self.parse_es,
                              headers={'User-Agent': self.ua, 'Referer': response.url},
                              meta={'es_url': response.urljoin(det_url)})

            es_next_page = response.xpath('//*[@id="paging"]/a[last()-1]/@href').extract_first()
            if es_next_page is not None:
                es_next_page = response.urljoin(es_next_page)
                yield Request(url=es_next_page, callback=self.parse,
                              headers={'User-Agent': self.ua, 'Referer': response.url})

    def parse_zf(self, response):
        zf_item = MaitianZufItem()
        zf_item['zf_url'] = response.meta.get('zf_url', None)
        zf_item['title'] = response.xpath('/html/body/section[2]/div[1]/h1/samp/text()').extract_first().strip()
        zf_item['rent'] = response.xpath('/html/body/section[2]/div[1]/table/tbody/tr[1]/td/strong/span/text()').extract_first() + '元/月'
        zf_item['floorage'] = response.xpath('/html/body/section[2]/div[1]/table/tbody/tr[3]/td[1]/text()').extract_first()
        zf_item['orientation'] = response.xpath('/html/body/section[2]/div[1]/table/tbody/tr[6]/td[1]/text()').extract_first()
        zf_item['decoration'] = response.xpath('/html/body/section[2]/div[1]/table/tbody/tr[5]/td[1]/text()').extract_first()
        zf_item['area'] = response.xpath('/html/body/section[2]/div[1]/table/tbody/tr[6]/td[1]/a/text()').extract_first()
        zf_item['way'] = response.xpath('/html/body/section[2]/div[1]/table/tbody/tr[8]/td/text()').extract_first()
        zf_item['comment'] = response.xpath('//label[@class="font_part"]/text()').extract_first()
        zf_item['house_type'] = replace(response.xpath('/html/body/section[2]/div[1]/table/tbody/tr[3]/td[2]/text()').extract_first())
        zf_item['payment'] = response.xpath('/html/body/section[2]/div[1]/table/tbody/tr[4]/td[2]/text()').extract_first()
        feature = response.xpath('/html/body/section[2]/div[1]/table/tbody/tr[5]/td[2]')
        zf_item['feature'] = replace(feature.xpath('string(.)').extract_first())
        zf_item['business'] = response.xpath('/html/body/section[2]/div[1]/table/tbody/tr[7]/td[2]/a/text()').extract_first()

        yield zf_item

    def parse_es(self, response):
        es_item = MaitianEsItem()
        es_item['es_url'] = response.meta.get('es_url', None)
        es_item['title'] = response.xpath('/html/body/section[2]/div[1]/h1/samp/text()').extract_first().strip()
        es_item['price'] = response.xpath('/html/body/section[2]/div[1]/table/tbody/tr[1]/td/strong/span/text()').extract_first() + '万/元'
        es_item['unit_pri'] = response.xpath('/html/body/section[2]/div[1]/table/tbody/tr[2]/td/text()').extract_first()
        es_item['down_payment'] = response.xpath('/html/body/section[2]/div[1]/table/tbody/tr[3]/td[1]/text()').extract_first()
        es_item['floorage'] = response.xpath('/html/body/section[2]/div[1]/table/tbody/tr[5]/td[1]/text()').extract_first()
        es_item['orientation'] = response.xpath('/html/body/section[2]/div[1]/table/tbody/tr[6]/td[1]/text()').extract_first()
        es_item['area'] = response.xpath('/html/body/section[2]/div[1]/table/tbody/tr[7]/td[1]/a/text()').extract_first()
        es_item['comment'] = response.xpath('//label[@class="font_part"]/text()').extract_first()
        es_item['monthly_pay'] = response.xpath('/html/body/section[2]/div[1]/table/tbody/tr[3]/td[2]/text()').extract_first()
        es_item['house_type'] = replace(response.xpath('/html/body/section[2]/div[1]/table/tbody/tr[5]/td[2]/text()').extract_first())
        es_item['floor'] = response.xpath('/html/body/section[2]/div[1]/table/tbody/tr[6]/td[2]/text()').extract_first()
        es_item['business'] = response.xpath('/html/body/section[2]/div[1]/table/tbody/tr[7]/td[2]/a/text()').extract_first()

        yield es_item