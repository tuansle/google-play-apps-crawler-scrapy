from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from items import GplaycrawlerItem
import urlparse
from scrapy.crawler import CrawlerProcess
import datetime
import csv


class MySpider(CrawlSpider):
    name = "playcrawler"
    allowed_domains = ["play.google.com"]
    start_urls = ["https://play.google.com/store/apps?hl=en"]
    rules = [Rule(LinkExtractor(allow=(r'apps',), deny=(r'reviewId')), follow=True, callback='parse_link')]

    # def __init__(self):
    #     dispatcher.connect(self.crawl_over, signals.spider_closed)
    #
    # def crawl_over(self, spider):
    #     f = open("linkfinaltest.txt", "w")
    #     f.write("\n".join(self.items))
    #     f.close()

    # init final list
    items = []

    # init filename
    filename = 1

    # r'page/\d+' : regular expression for http://isbullsh.it/page/X URLs
    # Rule(LinkExtractor(allow=(r'apps')),follow=True,callback='parse_link')]
    # r'\d{4}/\d{2}/\w+' : regular expression for http://isbullsh.it/YYYY/MM/title URLs
    def abs_url(url, response):
        """Return absolute link"""
        base = response.xpath('//head/base/@href').extract()
        if base:
            base = base[0]
        else:
            base = response.url
        return urlparse.urljoin(base, url)

    def parse_link(self, response):
        hxs = HtmlXPathSelector(response)
        titles = hxs.xpath('/html')
        for titles in titles:
            item = GplaycrawlerItem()
            item["Link"] = ''.join(titles.xpath('head/link[6]/@href').extract()).encode("utf-8")
            item["Item_name"] = ''.join(titles.xpath('//*[@class="document-title"]/div/text()').extract()).encode(
                "utf-8").replace("\n", ". ")
            item["Updated"] = ''.join(titles.xpath('//*[@itemprop="datePublished"]/text()').extract()).encode("utf-8").replace("\n", ". ")
            item["Author"] = ''.join(titles.xpath('//*[@itemprop="author"]/a/span/text()').extract()).encode("utf-8").replace("\n", ". ")
            item["Filesize"] = ''.join(titles.xpath('//*[@itemprop="fileSize"]/text()').extract()).encode("utf-8").replace("\n", ". ")
            item["Downloads"] = ''.join(titles.xpath('//*[@itemprop="numDownloads"]/text()').extract()).encode("utf-8").replace("\n", ". ")
            item["Version"] = ''.join(titles.xpath('//*[@itemprop="softwareVersion"]/text()').extract()).encode("utf-8").replace("\n", ". ")
            item["Compatibility"] = ''.join(titles.xpath('//*[@itemprop="operatingSystems"]/text()').extract()).encode(
                "utf-8").replace("\n", ". ")
            item["Content_rating"] = ''.join(titles.xpath('//*[@itemprop="contentRating"]/text()').extract()).encode(
                "utf-8").replace("\n", ". ")
            item["Author_link"] = ''.join(titles.xpath('//*[@class="dev-link"]/@href').extract()).encode(
                "utf-8").replace("\n", ". ")  # TODO: separate links and emails
            ##        item["Author_link_test"] = titles.xpath('//*[@class="content contains-text-link"]/a/@href').extract()
            item["Genre"] = ''.join(titles.xpath('//*[@itemprop="genre"]/text()').extract()).encode("utf-8").replace("\n", ". ")
            item["Price"] = ''.join(titles.xpath(
                '//*[@class="price buy id-track-click id-track-impression"]/span[2]/text()').extract()).encode(
                "utf-8").replace("\n", ". ")  # install mean free
            item["Rating_value"] = ''.join(titles.xpath('//*[@class="score"]/text()').extract()).encode("utf-8").replace("\n", ". ")
            item["Review_number"] = ''.join(titles.xpath('//*[@class="reviews-num"]/text()').extract()).encode("utf-8").replace("\n", ". ")
            item["Description"] = ''.join(titles.xpath('//*[@jsname="C4s9Ed"]//text()').extract()).encode("utf-8").replace("\n", ". ")
            item["IAP"] = ''.join(titles.xpath('//*[@class="inapp-msg"]/text()').extract()).encode("utf-8").replace("\n", ". ")
            item["Developer_badge"] = ''.join(titles.xpath('//*[@class="badge-title"]//text()').extract()).encode(
                "utf-8").replace("\n", ". ")
            item["Physical_address"] = ''.join(titles.xpath('//*[@class="content physical-address"]/text()').extract()).encode("utf-8").replace("\n", ". ")
            item["Video_URL"] = ''.join(titles.xpath('//*[@class="play-action-container"]/@data-video-url').extract()).encode("utf-8").replace("\n", ". ")
            item["Developer_ID"] = ''.join(titles.xpath('//*[@itemprop="author"]/a/@href').extract()).encode("utf-8").replace("\n", ". ")
            item["cover_image"] = ''.join(titles.xpath('//*[@class="cover-container"]/img/@src').extract()).encode("utf-8").replace("\n", ". ")
            item["screenshots"] = ''.join(titles.xpath('//*[@class="full-screenshot"]/@src').extract()).encode("utf-8").replace("\n", ". ")
            if item["Link"][46:49] == "com":
                # split package name out of link
                try:
                    item["package_name"] = item["Link"].split('=')[1]
                except Exception as e:
                    print e
                    pass

                # # split website and email address out of author link:
                # try:
                #     item["Author_site"], item["Author_email"] = \
                #         item["Author_link"].split("https://www.google.com/url?q=")[1].split("mailto:")
                # except:
                #     pass
                # print item
                self.items.append(item)

        if len(self.items) == 5000:
            filename = str(self.filename) + ".csv"
            self.filename += 1
            with open(filename, 'a') as csvfile:
                fieldnames = ['Video_URL',
                              'Author',
                              'Content_rating',
                              'Version',
                              'Filesize',
                              'screenshots',
                              'Updated',
                              'Description',
                              'Review_number',
                              'Downloads',
                              'Link',
                              'Genre',
                              'Developer_badge',
                              'Item_name',
                              'Rating_value',
                              'package_name',
                              'IAP',
                              'Physical_address',
                              'Author_link',
                              'Compatibility',
                              'Developer_ID',
                              'cover_image',
                              'Price']

                spamwriter = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=' ', quotechar='|', )
                spamwriter.writeheader()
                spamwriter.writerows(self.items)
                csvfile.close()
                spamwriter = None
            self.items = []



if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (X11; CrOS armv7l 9280.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3007.0 Safari/537.36'})
    spider = MySpider()
    process.crawl(spider)
    process.start()  # the script will block here
