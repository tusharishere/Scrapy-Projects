import scrapy


class BookstoreSpider(scrapy.Spider):
    name = "bookstore"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com"]

    def parse(self, response):
        books = response.xpath("//article[@class='product_pod']")
        for book in books:
            book_name = book.xpath(".//h3/a/text()").get()
            book_price =  book.xpath(".//p[@class='price_color']/text()").get()
            book_stock = book.xpath(".//div[@class='product_price']//p[@class='instock availability']/text()[2]").get().strip()
            book_url = book.xpath(".//div[@class='image_container']/a/@href").get()

            yield {
                'book_name':book_name,
                'book_price':book_price,
                'book_stock':book_stock,
                'book_url':response.urljoin(book_url)

            }
        next_page = response.xpath("//li[@class='next']/a/@href").get()     
        if next_page:
            yield scrapy.Request(response.urljoin(next_page),callback=self.parse)   
