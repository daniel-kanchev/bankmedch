import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from bankmedch.items import Article


class MedSpider(scrapy.Spider):
    name = 'med'
    start_urls = ['https://www.bankmed.ch/bankmed-news/']

    def parse(self, response):
        articles = response.xpath('//div[@class="vc_grid-item vc_clearfix vc_col-sm-12 vc_grid-item-zone-c-bottom"]')
        for article in articles:
            link = article.xpath('.//h3/a/@href').get()
            date = article.xpath('.//div[@class="vc_custom_heading article-date vc_gitem-post-data vc_gitem-post-data-source-post_date"]//text()').get()
            yield response.follow(link, self.parse_article, cb_kwargs=dict(date=date))

    def parse_article(self, response, date):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        if date:
            date = date.strip()
            # date = datetime.strptime(date.strip(), '')
            # date = date.strftime('%Y/%m/%d')

        content = response.xpath('(//div[@class="wpb_column pd-lft-mb pd-txt-20 vc_column_container vc_col-sm-12"])[2]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
