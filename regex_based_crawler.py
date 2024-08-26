import scrapy
import re

class CustomDomainSpider(scrapy.Spider):
    name = "custom_domain_spider"
    
    # Start URLs for different domains
    start_urls = [
        'http://siteone.com',  # Domain 1
        'http://sitetwo.com',  # Domain 2
    ]
    
    # Regex patterns for each domain
    domain_patterns = {
        'siteone.com': r'^https?://(www\.)?siteone\.com/.*$',
        'sitetwo.com': r'^https?://(www\.)?sitetwo\.com/.*$',
    }
    
    def parse(self, response):
        current_domain = response.url.split('/')[2]
        regex_pattern = self.domain_patterns.get(current_domain, None)

        if regex_pattern:
            all_links = response.css('a::attr(href)').getall()
            page_heading = response.css('title::text').get()  # Extract the page title

            # Yield the URL and the page title
            yield {
                'extracted_url': response.url,
                'page_title': page_heading
            }
            
            for link in all_links:
                full_url = response.urljoin(link)
                if re.match(regex_pattern, full_url):
                    yield scrapy.Request(full_url, callback=self.parse)

