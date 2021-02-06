import scrapy
from scrapy import *

class TripadvisorSpider(scrapy.Spider):
	name = 'tripadvisor'
	allowed_domains = ['tripadvisor.com']
	start_urls= (
		"https://www.tripadvisor.com.au/Restaurants-g255060-Sydney_New_South_Wales.html",
		)
	def parse(self, response):
		urls = response.xpath('//h3[@class="title"]/a[@class="property_title"]/@href').extract()
		print("Seyhan1")
		for url in urls:	
			absolute_url = response.urljoin(url)
			print(absolute_url)	
			yield scrapy.Request(absolute_url, 
				self.parse_restaurant)
			
		print("Seyhan2")	
		#next_page
		#next_page_url = response.xpath('//a[text()="Next"]').extract_first()
		#next_absolute_url = response.urljoin(next_page_url)
		#yield {"next_url", next_absolute_url}
		#yield scrapy.Request(next_absolute_url, callback = self.parse)

	def parse_restaurant(self, response):
		print("Seyhan")
		rating = response.xpath('//img[@property="ratingValue"]/@content').extract_first()
		#name = response.xpath('//div[@class="mapContainer"]/@data-name').extract_first()
		#latitute = response.xpath('//div[@class="mapContainer"]/@data-lat').extract_first()
		#logitude = response.xpath('//div[@class="mapContainer"]/@data-lng').extract_first()
		#url = response.xpath.urljoin
		yield {'Rating': rating}
		#yield {'Rating': rating,
		#'name': name,
		#'latitute': latitute,
		#'logitude': logitude,
		#'Url': url}
        

