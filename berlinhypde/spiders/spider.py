import scrapy

from scrapy.loader import ItemLoader

from ..items import BerlinhypdeItem
from itemloaders.processors import TakeFirst


class BerlinhypdeSpider(scrapy.Spider):
	name = 'berlinhypde'
	start_urls = ['https://www.berlinhyp.de/en/media/newsroom/latest-news?page_s10027=99999']

	def parse(self, response):
		post_links = response.xpath('//a[@class="d-block text-body"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="teaser col-lg-6 order-lg-first"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@class="date text-muted"]/text()').get()

		item = ItemLoader(item=BerlinhypdeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
