
from json.decoder import JSONDecodeError
import datetime
from datetime import datetime
from scrapy.spiders import SitemapSpider
class MultiSpider(SitemapSpider):
    name = "xy1"
    
    sitemap_urls = ["https://www.pwengraving.com/sitemap.xml"]
    
    
    # print(f'Scraping the following urls {start_urls}')

    def parse(self, response):
        component_to_xpath_dict = {"h1_tag": "//h1/text()",
                                   "title": "//title/text()",
                                   "meta_description": "//meta[@name='description']/@content",
                                   "image_src": "//img/@src",
                                   "image_alt": "//img/@alt",
        }
        result_json = {}
        result_json['url']=response.url
        print(f"response is {response.body}")
        for component in component_to_xpath_dict.keys():
            try:
                result_json[component] = response.xpath(component_to_xpath_dict[component]).getall()
                result_json[f'len_{component}'] = len(result_json[component][0])
            except:
                result_json[component] = ''
                result_json[f'len_{component}'] = -1
                pass
        # print(result_json)
        return result_json