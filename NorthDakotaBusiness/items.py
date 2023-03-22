# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NDbusinessItem(scrapy.Item):
    # fields for the item here
    business_name = scrapy.Field()
    filing_detail = scrapy.Field()
    
    pass