from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from items import GplaycrawlerItem
import urlparse
from scrapy.crawler import CrawlerProcess
import datetime
import csv
from misc import write_csv, open_csv, encode_str, standardize_string, decode_str


class MySpider(CrawlSpider):
    name = "playcrawler"
    custom_settings = {"DEPTH_LIMIT" : 15, # for 1GB computer
                       "RETRY_TIMES": 2}

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

        # download list (banned list of least download times)
        banned_download = ["None", None, " 15 ", " 510 ", " 1050 ", " 50100 ", " 100500 ", " 5001.000 ", " 1.0005.000 ", " 5.00010.000 ", " 10.00050.000 ", " 50.000100.000 "]
        for titles in titles:
            item = GplaycrawlerItem()
            item["Link"] = ''.join(titles.xpath('head/link[6]/@href').extract()).encode("utf-8")
            item["Item_name"] = encode_str(standardize_string(''.join(titles.xpath('//*[@class="document-title"]/div/text()').extract())))
            item["Updated"] = encode_str(standardize_string(''.join(titles.xpath('//*[@itemprop="datePublished"]/text()').extract())))
            item["Author"] = encode_str(standardize_string(''.join(titles.xpath('//*[@itemprop="author"]/a[1]/span/text()').extract())))
            item["Filesize"] = encode_str(standardize_string(''.join(titles.xpath('//*[@itemprop="fileSize"]/text()').extract())))
            item["Downloads"] = encode_str(standardize_string(''.join(titles.xpath('//*[@itemprop="numDownloads"]/text()').extract())))
            item["Version"] = encode_str(standardize_string(''.join(titles.xpath('//*[@itemprop="softwareVersion"]/text()').extract())))
            item["Compatibility"] = encode_str(standardize_string(''.join(titles.xpath('//*[@itemprop="operatingSystems"]/text()').extract())))
            item["Content_rating"] = encode_str(standardize_string(''.join(titles.xpath('//*[@itemprop="contentRating"]/text()').extract())))
            item["Author_link"] = encode_str(''.join(titles.xpath('//*[@class="dev-link"]/@href').extract()))
            item["Genre"] = encode_str(standardize_string(''.join(titles.xpath('//*[@itemprop="genre"]/text()').extract())))
            item["Price"] = encode_str(''.join(titles.xpath('//*[@class="price buy id-track-click id-track-impression"]/span[2]/text()').extract()))  # install mean free
            item["Rating_value"] = encode_str(standardize_string(''.join(titles.xpath('//*[@class="score"]/text()').extract())))
            item["Review_number"] = encode_str(standardize_string(''.join(titles.xpath('//*[@class="reviews-num"]/text()').extract())))
            item["Description"] = encode_str(standardize_string(''.join(titles.xpath('//*[@jsname="C4s9Ed"]//text()').extract())))
            item["IAP"] = encode_str(standardize_string(''.join(titles.xpath('//*[@class="inapp-msg"]/text()').extract())))
            item["Developer_badge"] = encode_str(standardize_string(''.join(titles.xpath('//*[@class="badge-title"]//text()').extract())))
            item["Physical_address"] = encode_str(standardize_string(''.join(titles.xpath('//*[@class="content physical-address"]/text()').extract())))
            item["Video_URL"] = ''.join(titles.xpath('//*[@class="play-action-container"]/@data-video-url').extract())
            item["Developer_ID"] = encode_str(standardize_string(''.join(titles.xpath('//*[@itemprop="author"]/a/@href').extract())))
            item["cover_image"] = ''.join(titles.xpath('//*[@class="cover-container"]/img/@src').extract())
            item["screenshots"] = ''.join(titles.xpath('//*[@class="full-screenshot"]/@src').extract())
            item["review_username1"] = encode_str(standardize_string(''.join(titles.xpath('//*[@data-expand-to="user-1"]/div[2]/span/text()').extract())))
            item["review_username2"] = encode_str(standardize_string(''.join(titles.xpath('//*[@data-expand-to="user-2"]/div[2]/span/text()').extract())))
            item["review_username3"] = encode_str(standardize_string(''.join(titles.xpath('//*[@data-expand-to="user-3"]/div[2]/span/text()').extract())))
            item["review_username4"] = encode_str(standardize_string(''.join(titles.xpath('//*[@data-expand-to="user-4"]/div[2]/span/text()').extract())))
            item["review_star1"] = encode_str(standardize_string(''.join(titles.xpath('//*[@data-expand-to="user-1"]/div[2]/div[1]/div[1]/@aria-label').extract())))
            item["review_star2"] = encode_str(standardize_string(''.join(titles.xpath('//*[@data-expand-to="user-2"]/div[2]/div[1]/div[1]/@aria-label').extract())))
            item["review_star3"] = encode_str(standardize_string(''.join(titles.xpath('//*[@data-expand-to="user-3"]/div[2]/div[1]/div[1]/@aria-label').extract())))
            item["review_star4"] = encode_str(standardize_string(''.join(titles.xpath('//*[@data-expand-to="user-4"]/div[2]/div[1]/div[1]/@aria-label').extract())))
            item["review_content1"] = encode_str(standardize_string(''.join(titles.xpath('//*[@data-expand-to="user-1"]/div/div[2]/div/text()').extract())))
            item["review_content2"] = encode_str(standardize_string(''.join(titles.xpath('//*[@data-expand-to="user-2"]/div/div[2]/div/text()').extract())))
            item["review_content3"] = encode_str(standardize_string(''.join(titles.xpath('//*[@data-expand-to="user-3"]/div/div[2]/div/text()').extract())))
            item["review_content4"] = encode_str(standardize_string(''.join(titles.xpath('//*[@data-expand-to="user-4"]/div/div[2]/div/text()').extract())))
            # item["test"] = ''.join(titles.xpath('//*[@data-expand-to="user-1"]/div[2]/div[1]/div[1]/@aria-label').extract())
            if item["Link"][0:46] == "https://play.google.com/store/apps/details?id=":
                # split package name out of link
                try:
                    item["package_name"] = item["Link"].split('=')[1]
                except Exception as e:
                    print e
                    pass

                # only take apps has download more than xx
                if item["Downloads"] not in banned_download:
                #     print #debug
                    self.items.append(item)

        if len(self.items) == 2000:    # 5000 for 1GB computer
            filename = str(self.filename) + ".csv"
            self.filename += 1

            # write to file
            write_csv(csv_path=filename, list_to_write=self.items)
            self.items = []



if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (X11; CrOS armv7l 9280.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3007.0 Safari/537.36'})
    spider = MySpider()
    process.crawl(spider)
    process.start()  # the script will block here
