
import scrapy 
from scrapy.crawler import CrawlerProcess

class mySpide(scrapy.Spider):
    name = 'quoteScraper'
    unique_value = 0
    def start_requests(self):
        url ="https://quotes.toscrape.com/"
        yield scrapy.Request(url=url,callback=self.parse)
    def parse(self,response):
        self.unique_value += 1
        allQuotes = response.css('div.quote')
        for i in range(len(allQuotes)):
            quotes = allQuotes[i].css('span.text::text').extract_first()
            author = allQuotes[i].css('small.author::text').extract_first()
            tags = allQuotes[i].css('div.tags a.tag::text').extract()
            neww=str(self.unique_value)+str(i)
            data = {'pkk':neww,'quote':quotes,'author':author,'tags':tags}
            # Here yield data does all the magic. This line returns the scraped info(the dictionary of quotes, authors, etc.) to scrapy which in turn processes it and stores it.
            # https://www.analyticsvidhya.com/blog/2017/07/web-scraping-in-python-using-scrapy/
            yield data
        navigation = response.css('nav li.next>a::attr(href)').extract_first()
        # print("MY NAV: ",navigation)
        if navigation:
            next_page = response.urljoin(navigation)
            # Scrapy has built in duplicate filtering which is turned on by default, now we've turned off
            yield scrapy.Request(next_page, callback=self.parse,dont_filter=True)
            # this is another way, here we donot have to join relative path (to absolute)
            # yield response.follow(url=navigation,callback=self.parse)


# driver code
# globalLst = []
# process = CrawlerProcess()
# process.crawl(mySpide)
# process.start()

# print("At last: ",globalLst)