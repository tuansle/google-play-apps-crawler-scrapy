# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

# from scrapy.item import Item, Field
import scrapy


class GplaycrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = Field()
    Link = scrapy.Field()
    Item_name = scrapy.Field()
    Updated = scrapy.Field()
    Author = scrapy.Field()
    Filesize = scrapy.Field()
    Downloads = scrapy.Field()
    Version = scrapy.Field()
    Compatibility = scrapy.Field()
    Content_rating = scrapy.Field()
    Author_link = scrapy.Field()
    ##    Author_link_test = scrapy.Field()
    Genre = scrapy.Field()
    Genre2 = scrapy.Field()
    Price = scrapy.Field()
    Rating_value = scrapy.Field()
    Review_number = scrapy.Field()
    Description = scrapy.Field()
    IAP = scrapy.Field()
    Developer_badge = scrapy.Field()
    Physical_address = scrapy.Field()
    Video_URL = scrapy.Field()
    Developer_ID = scrapy.Field()
    # add by Tuan
    cover_image = scrapy.Field()
    screenshots = scrapy.Field()
    package_name = scrapy.Field()
    test=scrapy.Field()
    review_username1=scrapy.Field()
    review_star1=scrapy.Field()
    review_content1=scrapy.Field()
    review_username2=scrapy.Field()
    review_star2=scrapy.Field()
    review_content2=scrapy.Field()
    review_username3=scrapy.Field()
    review_star3=scrapy.Field()
    review_content3=scrapy.Field()
    review_username4=scrapy.Field()
    review_star4=scrapy.Field()
    review_content4=scrapy.Field()
    # Author_site = scrapy.Field()
    # Author_email = scrapy.Field()


