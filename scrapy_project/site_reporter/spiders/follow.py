"""Scrapy spider to get the links for a website"""
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError, TimeoutError, TCPTimedOutError
from twisted.python.failure import Failure

from site_reporter.items import SiteReporterItem


class FollowAllSpider(CrawlSpider):
    """Spider properties and methods"""
    name = "follow_all"

    # Only scrape on pages within the crawler-test.com domain
    allowed_domains = ["crawler-test.com"]

    # This is the list of URLs to be scrapped
    start_urls = ["https://crawler-test.com"]

    # Setting scrapy to follow all links
    rules = [Rule(LinkExtractor(), callback="parse", follow=True, errback="parse_error")]


    def parse(self, response):
        self.logger.debug(f"Scrapping the page: {response.url}")

        # Iterating over the links available in the page
        for link in response.xpath("//a"):
            href_to_save= link.xpath("./@href").get()

            # Avoiding the root page and links to popups
            if href_to_save not in ["/", "#"]:
                self.logger.debug(f"The page has a link to another page: {href_to_save}")
                # Getting the link information
                link_text = link.xpath("./text()").get()

                depth = response.meta.get("depth", 0)
                self.logger.debug("%s: depth is %s", href_to_save, depth)

                # Output
                item = SiteReporterItem()
                item["title"] = link_text
                item["link"] = href_to_save
                item["error"] = "None"
                item["depth"] = depth
                yield item


    def parse_error(self, failure: Failure) -> None:
        """log all failures"""
        url = ""
        title = ""
        depth = 0
        failure.check()
        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error("HttpError on %s", response.url)
            url = response.url
            title = "HttpError"
            depth = response.meta.get("depth", 0)
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error("DNSLookupError on %s", request.url)
            url = request.url
            title = "DNSLookupError"
            depth = request.meta.get("depth", 0)
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error("TimeoutError on %s", request.url)
            url = request.url
            title = "TimeoutError"
            depth = request.meta.get("depth", 0)
        else:
            url = failure.value.response.url
            title = url
            depth = failure.value.response.meta.get("depth", 0)
            self.logger.error("%s on %s", failure.getErrorMessage(), url)

        # Output
        item = SiteReporterItem()
        item["title"] = title
        item["link"] = url
        item["error"] = failure.getErrorMessage()
        item["depth"] = depth
        yield item
