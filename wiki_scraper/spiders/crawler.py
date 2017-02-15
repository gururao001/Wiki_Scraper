from scrapy.selector import Selector
from scrapy import Spider
from wiki_scraper.items import wiki_scraperItem
from scrapy.spider import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request


import re
import os
import sys

# Path variable
PATH = os.path.abspath(os.path.join(os.path.dirname('__file__'), os.path.pardir))
sys.path.append(PATH)




# class representing the spider
class wiki_scraperspider(CrawlSpider):
	name="wikipedia"
	allowed_domains = ["https://en.wikipedia.org", "en.wikipedia.org", "wikipedia.org",]
	
	#Follow links till we get all the pages
	rules = (#Rule(LinkExtractor(allow = (),restrict_xpaths=('//*[contains(concat( " ", @class, " " ), concat( " ", "CategoryTreeLabelCategory", " " ))]')),follow = True),
			#Rule(LinkExtractor(allow = (),restrict_xpaths=('//*[(@id = "mw-pages")]//*[contains(concat( " ", @class, " " ), concat( " ", "mw-category-group", " " ))]//a')),callback = 'parse_2',follow = False),
			#Rule(LinkExtractor(allow = (),restrict_xpaths=('//*[contains(concat( " ", @class, " " ), concat( " ", "mw-category-group", " " ))]//a')),follow = False),



			)
	

	def __init__(self, filename = "../../list_of_categories.txt", *args, **kwargs):
		super(wiki_scraperspider, self).__init__(*args, **kwargs)
		self.filename = filename
	



# Start url requests based on categories from text file
	def start_requests(self):
		catagories = ['Machine_learning', 'Business_software', 'UEFA_Champions_League']
		for entry in catagories:
			url = ''.join(('https://en.wikipedia.org/wiki/Category:',entry))
			yield Request(url,self.parse)	
	


# Parsing logic. Extract all that necessary using XPATH selector. All the text data are available in pages in the bottom of category. Get its URL and extract text

	def parse(self, response):
		

		categories_letters = response.xpath('//div[@id="mw-pages"]/div/div/div[@class="mw-category-group"]')
		for letter in categories_letters:
			letter_name = ''.join(letter.xpath('.//h3/text()').extract()).replace(u'\xa0', u'')
			for category in letter.xpath('.//ul/li/a'):
				category_name = ''.join(category.xpath('.//@title').extract())
				category_url = ''.join(category.xpath('.//@href').extract())
				title = category_name
				url = category_url
				letter = letter_name
				yield Request(
					url = ''.join(('https://en.wikipedia.org',url)),
					callback = self.parse_text,
					meta = {'title':title, 'url':url, 'letter':letter} 
						)		


	def parse_text(self,response):
		item = wiki_scraperItem()
		sel = Selector(response)
		item['text'] = sel.xpath('//p/text()').extract()
		item['title'] = response.meta['title']
		#item['url'] = response.meta['url']
		item['letter'] = response.meta['letter']
		yield item
		






