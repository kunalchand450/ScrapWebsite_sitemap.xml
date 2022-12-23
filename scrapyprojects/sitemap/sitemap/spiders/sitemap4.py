import json
import os
import tempfile 
import scrapy
import pandas
from bs4 import BeautifulSoup
from json.decoder import JSONDecodeError
import datetime
from datetime import datetime
from lxml import etree
from datetime import datetime
from scrapy.spiders import SitemapSpider
class MultiSpider(SitemapSpider):
    name = "xy12"
    # custom_settings = {
    #     'LOG_LEVEL': 'CRITICAL',
    # }
    
    # sitemap_urls = ["https://stagum.com/sitemap_index.xml"]
    # sitemap_urls = ["https://www.pwengraving.com/sitemap.xml"]
    sitemap_urls = ["https://www.thefocaltherapyclinic.co.uk/sitemap_index.xml"] 

    def parse(self, response):
        component_to_xpath_dict = {"h1_tag_wordpress": "//h1/text()",
                                    "h1_tag_magento": "//h1/span/text()",
                                   "title": "//title/text()",
                                   "meta_description": "//meta[@name='description']/@content",
                                   "meta_keyword": '//meta[@name="keywords"]/@content',
                                   "image_data": "//img"
        }
        result_json={}
        result_json['url']=response.url
        for component in component_to_xpath_dict.keys():
            try:
                result_json[component] = response.xpath(component_to_xpath_dict[component]).getall()
                result_json[f'len_{component}'] = len(result_json[component][0])
            except:
                result_json[component] = ''
                result_json[f'len_{component}'] = -1
                pass
        image_data_list = []
        for image_data in result_json['image_data']:
            current_src = etree.HTML(str(BeautifulSoup(image_data))).xpath("//@src")
            current_alt = etree.HTML(str(BeautifulSoup(image_data))).xpath("//@alt")
            image_data_list.append([current_src[0], current_alt[0] if current_alt else ''])
            result_json['image_data'] = image_data_list

        return result_json
