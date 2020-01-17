import scrapy

from ..items import ProductScraperItem


class EcomSpider(scrapy.Spider):
    name = 'ecom_spider'
    allowed_domains = ['clever-lichterman-044f16.netlify.com/']

    def start_requests(self):
        start_urls = [
            'https://clever-lichterman-044f16.netlify.com/products/taba-cream.1/'
        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = ProductScraperItem()
        item['product_url'] = response.url
        item['price'] = response.css("div.my-4 span::text").get()
        item['title'] = response.css("div.col-lg-5.offset-lg-1 h4::text").get()
        item['img_url'] = response.css("img.img-fluid.w-100::attr(src)").get()
        return item
