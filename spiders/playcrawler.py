from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from items import GplaycrawlerItem
import urlparse
from scrapy.crawler import CrawlerProcess
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy import Request
from scrapy.http import FormRequest
import scrapy


class MySpider(CrawlSpider):
    name = "playcrawler"
    allowed_domains = ["play.google.com", "accounts.google.com"]
    start_urls = ["https://play.google.com/store/apps?hl=en"]
    rules = [Rule(LinkExtractor(allow=(r'apps'), deny=(r'reviewId')), follow=True, callback='parse_link')]

    logintry = 1
    logintry2 = 1

    # def __init__(self):
    #     dispatcher.connect(self.crawl_over, signals.spider_closed)
    #
    # def crawl_over(self, spider):
    #     f = open("linkfinaltest.txt", "w")
    #     f.write("\n".join(self.items))
    #     f.close()

    # init final list
    items = []

    # r'page/\d+' : regular expression for http://isbullsh.it/page/X URLs
    # Rule(LinkExtractor(allow=(r'apps')),follow=True,callback='parse_link')]
    # r'\d{4}/\d{2}/\w+' : regular expression for http://isbullsh.it/YYYY/MM/title URLs

    def start_requests(self):
        yield Request(
            url='https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fplay.google.com%2Fstore%2Fapps%3Fhl%3Den&followup=https%3A%2F%2Fplay.google.com%2Fstore%2Fapps%3Fhl%3Den&hl=en&passive=1209600&service=googleplay&flowName=GlifWebSignIn&flowEntry=ServiceLogin',
            callback=self.login)

    def login(self, response):
        """
        Insert the email. Next, go to the password page.
        """
        if self.logintry <= 2:
            yield FormRequest.from_response(
                response,
                formdata={'identifier': 'downloadxender@gmail.com'},
                callback=self.login,
                dont_filter=True)
            self.logintry += 1
        else:
            yield FormRequest.from_response(response, formdata={'identifier': 'downloadxender@gmail.com'},
                                            dont_filter=True, callback=self.log_password)

    def log_password(self, response):
        """
        Enter the password to complete the log in.
        
        """
        if self.logintry2 <= 2:
            yield FormRequest.from_response(
                response,
                formdata={'password': '123gmkhoe'},
                callback=self.log_password,
                dont_filter=True)
            self.logintry2 += 1

        else:
            yield Request(url = "https://play.google.com/store/apps",
                                            dont_filter=True, callback=self.parse_link)

    def abs_url(url, response):
        """Return absolute link"""
        base = response.xpath('//head/base/@href').extract()
        if base:
            base = base[0]
        else:
            base = response.url
        return base

    link = []
    def parse_link(self, response):
        print self.abs_url(response)
        hxs = HtmlXPathSelector(response)
        titles = hxs.xpath('/html')
        for titles in titles:
            item = GplaycrawlerItem()
            item["Link"] = ''.join(titles.xpath('head/link[6]/@href').extract()).encode("utf-8")
            item["Item_name"] = ''.join(titles.xpath('//*[@class="document-title"]/div/text()').extract()).encode(
                "utf-8")
            item["Updated"] = ''.join(titles.xpath('//*[@itemprop="datePublished"]/text()').extract()).encode("utf-8")
            item["Author"] = ''.join(titles.xpath('//*[@itemprop="author"]/a/span/text()').extract()).encode("utf-8")
            item["Filesize"] = ''.join(titles.xpath('//*[@itemprop="fileSize"]/text()').extract()).encode("utf-8")
            item["Downloads"] = ''.join(titles.xpath('//*[@itemprop="numDownloads"]/text()').extract()).encode("utf-8")
            item["Version"] = ''.join(titles.xpath('//*[@itemprop="softwareVersion"]/text()').extract()).encode("utf-8")
            item["Compatibility"] = ''.join(titles.xpath('//*[@itemprop="operatingSystems"]/text()').extract()).encode(
                "utf-8")
            item["Content_rating"] = ''.join(titles.xpath('//*[@itemprop="contentRating"]/text()').extract()).encode(
                "utf-8")
            item["Author_link"] = ''.join(titles.xpath('//*[@class="dev-link"]/@href').extract()).encode(
                "utf-8")  # TODO: separate links and emails
            ##        item["Author_link_test"] = titles.xpath('//*[@class="content contains-text-link"]/a/@href').extract()
            item["Genre"] = ''.join(titles.xpath('//*[@itemprop="genre"]/text()').extract()).encode("utf-8")
            item["Price"] = ''.join(titles.xpath(
                '//*[@class="price buy id-track-click id-track-impression"]/span[2]/text()').extract()).encode(
                "utf-8")  # install mean free
            item["Rating_value"] = ''.join(titles.xpath('//*[@class="score"]/text()').extract()).encode("utf-8")
            item["Review_number"] = ''.join(titles.xpath('//*[@class="reviews-num"]/text()').extract()).encode("utf-8")
            item["Description"] = ''.join(titles.xpath('//*[@jsname="C4s9Ed"]//text()').extract()).encode("utf-8")
            item["IAP"] = ''.join(titles.xpath('//*[@class="inapp-msg"]/text()').extract()).encode("utf-8")
            item["Developer_badge"] = ''.join(titles.xpath('//*[@class="badge-title"]//text()').extract()).encode(
                "utf-8")
            item["Physical_address"] = ''.join(
                titles.xpath('//*[@class="content physical-address"]/text()').extract()).encode("utf-8")
            item["Video_URL"] = ''.join(
                titles.xpath('//*[@class="play-action-container"]/@data-video-url').extract()).encode("utf-8")
            item["Developer_ID"] = ''.join(titles.xpath('//*[@itemprop="author"]/a/@href').extract()).encode("utf-8")
            item["cover_image"] = ''.join(titles.xpath('//*[@class="cover-container"]/img/@src').extract()).encode(
                "utf-8")
            item["screenshots"] = ''.join(titles.xpath('//*[@class="full-screenshot"]/@src').extract()).encode("utf-8")
            if item["Link"][46:49] == "com":
                # split package name out of link
                try:
                    item["package_name"] = item["Link"].split('=')[1]
                except Exception as e:
                    print e
                    pass
                # split website and email address out of author link:
                try:
                    item["Author_site"], item["Author_email"] = \
                        item["Author_link"].split("https://www.google.com/url?q=")[1].split("mailto:")
                except:
                    pass
                # print item
                self.items.append(item)

                # write to file using csvwriter
                # f = open("linkfinaltest.txt", "a")
                # f.write("%s,%s,%s\n" % item["Item_name"], item["Updated"], item["Author"], item["Filesize"],
                #         item["Downloads"], item["Version"], item["Compatibility"], item["Content_rating"],
                #         item["Genre"], item["Price"], item["Rating_value"], item["Review_number"],
                #         item["Description"], item["IAP"], item["Developer_badge"], item["Physical_address"])
                # f.close()
            return self.items


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (X11; CrOS armv7l 9280.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3007.0 Safari/537.36'})
    spider = MySpider()
    process.crawl(spider)
    process.start()  # the script will block here
