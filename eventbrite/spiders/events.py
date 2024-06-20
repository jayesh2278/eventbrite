import scrapy
from urllib.parse import urlparse


class ExampleSpider(scrapy.Spider):
    name = 'events'
    start_urls = [
        'https://www.eventbrite.com/d/ny--new-york/alternative-protein/?page=1',
        'https://www.eventbrite.com/d/united-states/alternative-protein/?bbox=34.742515899999944%2C32.029252%2C34.8519761%2C32.146611&page=1'
        ]

    def parse(self, response):
        loc_url = response.meta.get("loc_url", response.url)
        count = response.meta.get("count", 1)
        
        next_flag = True
        end_text = response.xpath('.//div[text()="Nothing matched your search, but you might like these options."]').get()
        if end_text:
            next_flag = False
            
        for url in response.xpath('.//ul[contains(@class, "search-main-content")]//.//a[@class="eds-event-card-content__action-link" and @tabindex="0" and @rel="noopener"]/@href').getall():
            yield scrapy.Request(url,callback=self.parse_detail)
        
        if next_flag:
            count = count + 1
            url = loc_url.split('page=', 1)[0]
            url = f'{url}page={count}'
            yield scrapy.Request(
                url=url,
                meta={
                    'loc_url': loc_url, 
                    "count": count},
                callback=self.parse
                )

    def parse_detail(self,response):
        title = response.xpath('.//h1/text()').get()
        image = response.xpath('.//picture//img/@src').get()

        date_time = response.xpath('.//div[@class="date-and-time"]//text()').getall()
        if not date_time:
            date_time = response.xpath('.//*[@class="start-date"]/text()').getall()
        date_time = ''.join(date_time).strip()
        
        location = response.xpath('.//h3[text()="Location"]/../following-sibling::p/text()').getall()
        location = ','.join(location).strip()

        all_text = response.xpath('.//div[h2[text()="About this event"]]/div//text()').getall()
        if not all_text:
            all_text = response.xpath('.//div[h2[text()="About this event"]]/following-sibling::div//text()').getall()
        all_text = ''.join(all_text).strip().replace('\n',' ')

        tags = response.xpath('.//h3[text()="Tags"]/../following-sibling::ul//text()').getall()
        tags = ','.join(tags).strip()  

        event_url= response.url    

        yield{
            'title':title,
            'image':image,
            'event_url':event_url,
            'date_time':date_time,
            'location':location,
            'all_text':all_text,
            'tags':tags
        }
        