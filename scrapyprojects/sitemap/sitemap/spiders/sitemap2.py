from scrapy.spiders import SitemapSpider
class MySpider(SitemapSpider):
    name = "xyz"
    # allowed_domains = ["discoverwebtech.com"]
    sitemap_urls = ["https://discoverwebtech.com/sitemap_index.xml"] 
    def parse(self, response):
        item={}
        item['url']=response.url

        item['h1_tag'] = response.xpath("//h1/text()").getall()
        item['title'] = response.xpath("//title/text()").get()
        item['meta_description'] = response.xpath("//meta[@name='description']/@content").get()
        item['len_img_tag'] = len(response.xpath("//img").getall())
        item['image_src'] = response.xpath("//img/@src").getall()
        item['image_alt'] = response.xpath("//img/@alt").getall()
        

        # item['len_title'] = len(response.xpath("//title/text()").get())
        # item['len_h1_tag'] = len(response.xpath("//h1/text()").get())
        # item['len_meta_description'] = len(response.xpath("//meta[@name='description']/@content").get())
        # item['len_image_src'] = len(response.xpath("//img/@src").getall())
        # item['len_image_alt'] = len(response.xpath("//img/@alt").getall())
        return item
        
    
