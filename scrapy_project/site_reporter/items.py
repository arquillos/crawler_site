"""Model for the scraped item"""
import scrapy


class SiteReporterItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    error = scrapy.Field()
    depth = scrapy.Field()
