from scrapy import Spider,Request
from jingdong.items import JingdongItem,IdItem
import json
import re


class JingdongSpider(Spider):
    name = 'jingdong'
    allowed_domains = []
    headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding':'gzip, deflate, br',
        'Connection':'keep - alive',
        'Upgrade-Insecure-Requests':'1',
    }

    def start_requests(self):
        start_urls = ['https://search.jd.com/Search?keyword=%E6%96%87%E8%83%B8&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.his.0.0&page={}&s=1&click=0'.format(str(i)) for i in range(1,150,2)]
        for url in start_urls:
            yield Request(url=url, headers= self.headers, callback=self.parse)


    def parse(self, response):
        selector = response.xpath('//ul[@class="gl-warp clearfix"]/li')
        id_list = []
        for info in selector:
            try:
                id = info.xpath('@data-sku').extract_first()
                if id not in id_list:
                    id_list.append(id)
                    item = IdItem()
                    item['id'] = id
                    comment_url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv6&productId={}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1'.format(str(id))
                    yield Request(url=comment_url, meta={'item':item}, headers=self.headers, callback=self.parseurl)
            except IndexError:
                continue

    def parseurl(self,response):
        t = re.findall('^fetchJSON_comment98vv\d*\((.*)\);', response.text)  # 去掉json的头信息,变成一个单一的列表
        json_data = json.loads(t[0])  # 字符串格式变成json格式
        page = json_data['maxPage']
        item = response.meta['item']
        id = item['id']
        urls = ['https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv6&productId={}&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1'.format(str(id), str(i)) for i in range(0, int(page))]

        for path in urls:
            yield Request(url=path, headers=self.headers, callback=self.parsebody)

    def parsebody(self,response):
        t = re.findall('^fetchJSON_comment98vv\d*\((.*)\);', response.text)  # 去掉json的头信息,变成一个单一的列表
        json_data = json.loads(t[0])

        for comment in json_data['comments']:  # 列表套字典格式
            item = JingdongItem()
            try:
                item['content'] = comment['content']
                item['creationTime'] = comment['creationTime']
                item['productColor'] = comment['productColor']
                item['productSize'] = comment['productSize']
                item['userClientShow'] = comment['userClientShow']
                item['userLevelName'] = comment['userLevelName']
                yield item
            except:
                continue

















