import scrapy

class DomainSpider(scrapy.Spider):
    name = 'domain'
    allowed_domains = ['domain.com.au']
    
    # Starting URL (modify this to the specific search page you want to crawl)
    start_urls = [
        'https://www.domain.com.au/sale/sydney-nsw-2000/'
    ]
    
    def parse(self, response):
        # Extract property containers
        property_cards = response.css('div.css-1nj9ymt')

        for card in property_cards:
            # Extract data from each property card
            title = card.css('h2.css-1rhznz4 a::text').get()
            price = card.css('p.css-mgq8yx::text').get()
            address = card.css('span.css-164r41r::text').get()
            url = card.css('h2.css-1rhznz4 a::attr(href)').get()

            # Yield the scraped information
            yield {
                'title': title,
                'price': price,
                'address': address,
                'url': response.urljoin(url)
            }

        # Pagination: Follow the next page link
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

