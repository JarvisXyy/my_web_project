# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WenxuanevItem(scrapy.Item):
    title = scrapy.Field() #文章标题
    article_time = scrapy.Field() #文章发布时间
    author = scrapy.Field() #文章作者
