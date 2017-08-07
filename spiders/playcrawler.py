from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from items import GplaycrawlerItem
import urlparse
from scrapy.crawler import CrawlerProcess


class MySpider(CrawlSpider):
  name = "playcrawler"
  allowed_domains = ["play.google.com"]
  start_urls = ["https://play.google.com/store/apps?hl=en"]
  rules = [Rule(LinkExtractor(allow=(r'apps',),deny=(r'reviewId')),follow=True,callback='parse_link')]
    	# r'page/\d+' : regular expression for http://isbullsh.it/page/X URLs
    	#Rule(LinkExtractor(allow=(r'apps')),follow=True,callback='parse_link')]
    	# r'\d{4}/\d{2}/\w+' : regular expression for http://isbullsh.it/YYYY/MM/title URLs
  def abs_url(url, response):
      """Return absolute link"""
      base = response.xpath('//head/base/@href').extract()
      if base:
        base = base[0]
      else:
        base = response.url
      return urlparse.urljoin(base, url)
    
  def parse_link(self,response):
      hxs = HtmlXPathSelector(response)
      titles = hxs.select('/html')
      items = []
      for titles in titles :
        item = GplaycrawlerItem()
        item["Link"] = ''.join(titles.select('head/link[6]/@href').extract())
        item["Item_name"] = ''.join(titles.select('//*[@class="document-title"]/div/text()').extract())
        item["Updated"] = ''.join(titles.select('//*[@itemprop="datePublished"]/text()').extract())
        item["Author"] = ''.join(titles.select('//*[@itemprop="author"]/a/span/text()').extract())
        item["Filesize"] = ''.join(titles.select('//*[@itemprop="fileSize"]/text()').extract())
        item["Downloads"] = ''.join(titles.select('//*[@itemprop="numDownloads"]/text()').extract())
        item["Version"] = ''.join(titles.select('//*[@itemprop="softwareVersion"]/text()').extract())
        item["Compatibility"] = ''.join(titles.select('//*[@itemprop="operatingSystems"]/text()').extract())
        item["Content_rating"] = ''.join(titles.select('//*[@itemprop="contentRating"]/text()').extract())
        item["Author_link"] = ''.join(titles.select('//*[@class="dev-link"]/@href').extract())  # TODO: separate links and emails
##        item["Author_link_test"] = titles.select('//*[@class="content contains-text-link"]/a/@href').extract()
        item["Genre"] = ''.join(titles.select('//*[@itemprop="genre"]/text()').extract())
        item["Price"] = ''.join(titles.select('//*[@class="price buy id-track-click id-track-impression"]/span[2]/text()').extract()) #install mean free
        item["Rating_value"] = ''.join(titles.select('//*[@class="score"]/text()').extract())
        item["Review_number"] = ''.join(titles.select('//*[@class="reviews-num"]/text()').extract())
        item["Description"] = ''.join(titles.select('//*[@jsname="C4s9Ed"]//text()').extract())
        item["IAP"] = ''.join(titles.select('//*[@class="inapp-msg"]/text()').extract())
        item["Developer_badge"] = ''.join(titles.select('//*[@class="badge-title"]//text()').extract())
        item["Physical_address"] = ''.join(titles.select('//*[@class="content physical-address"]/text()').extract())
        item["Video_URL"] = ''.join(titles.select('//*[@class="play-action-container"]/@data-video-url').extract())
        item["Developer_ID"] = ''.join(titles.select('//*[@itemprop="author"]/a/@href').extract())
        item["cover_image"] = ''.join(titles.select('//*[@class="cover-container"]/img/@src').extract())
        if item["Link"][46:49] == "com":
            print item
            items.append(item)
        return items


if __name__ == "__main__":
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/5.0 (X11; CrOS armv7l 9280.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3007.0 Safari/537.36'})
    spider = MySpider()
    process.crawl(spider)
    process.start()  # the script will block here

