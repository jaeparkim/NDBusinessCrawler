import json
import scrapy

from scrapy.http import JsonRequest
from scrapy.crawler import CrawlerProcess

from NorthDakotaBusiness.items import NDbusinessItem


class NdbusinessSpider(scrapy.Spider):
    name = 'ndbusiness'

    def start_requests(self):
        url = 'https://firststop.sos.nd.gov/api/Records/businesssearch'
        payload = {
            'SEARCH_VALUE': 'X',
            'STARTS_WITH_YN': True,
            'ACTIVE_ONLY_YN': True,
            }

        req = JsonRequest(
            url=url,
            method='POST',
            callback=self.parse,
            body=json.dumps(payload)
        )

        yield req

    def parse(self, response):
        res = json.loads(response.body)
        columns = ['TITLE', 'ID', 'FILING_DATE', 'RECORD_NUM', 'STATUS']

        data = res.get('rows')
        dbID = data.keys()
      
        for _id in dbID:
            # item defined in ../items.py
            item = NDbusinessItem()
            
            # some names of business in data doesn't start w/ X
            if data[_id]['TITLE'][0].startswith('X'):
                item['business_name'] = data[_id]['TITLE']
                business_url = f'https://firststop.sos.nd.gov/api/FilingDetail/business/{_id}/false'
                yield scrapy.Request(business_url,
                                    callback=self.parse_business_info,
                                    cb_kwargs={'item': item},
                                    method='GET',
                                    headers={'accept': '*/*', 'authorization': 'undefined'})

    def parse_business_info(self, response, item):
        res = json.loads(response.body)
        business_filing_details = res.get('DRAWER_DETAIL_LIST')

        # fill in the item defined in ../items.py
        item['filing_detail'] = dict((entry['LABEL'], entry['VALUE']) for entry in business_filing_details)
        yield item


if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(NdbusinessSpider)
    process.start()
