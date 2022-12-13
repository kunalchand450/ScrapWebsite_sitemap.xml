import json
import os
import tempfile 
import scrapy
import pandas
from json.decoder import JSONDecodeError
import datetime
from datetime import datetime
from lxml import etree
from bs4 import BeautifulSoup
from scrapy.spiders import SitemapSpider

class MultiSpider(SitemapSpider):
    name = "sitemapspider"
    # custom_settings = {
    #     'LOG_LEVEL': 'CRITICAL',
    # }
    sitemap_urls = ["https://discoverwebtech.com/sitemap_index.xml"]
    start_urls = []
    # with open(('/tmp/sites_file'), 'r') as read_obj:
    #     for line in read_obj.readlines():
    #         start_urls.append(f"http://www.{line.strip().lstrip('www.')}")
    # # start_urls = ["http://www.adara.com", "https://stagum.com/", "http://www.anacostiatrails.org", "http://www.aqua.org", "http://www.baltimore.org", "http://www.baltimorecountymd.gov", "http://www.beachesbayswaterways.org", "http://www.berlinmd.gov", "http://www.bluum.com", "http://www.bwbwi.com", "http://www.calvertcountymd.gov", "http://www.carrollbiz.org", "http://www.carrollcountymd.gov", "http://www.celticrnr.com", "http://www.chesapeakebaymagazine.com", "http://www.co.pg.md.us", "http://www.co.worcester.md.us", "http://www.danikapr.com", "http://www.delmarvadiscoverycenter.org", "http://www.docogonet.com", "http://www.e.hps.com", "http://www.enradius.com", "http://www.expediagroup.com", "http://www.flyingdog.com", "http://www.fogo.com", "http://www.harfordbrewtours.com", "http://www.havredegracemd.com", "http://www.higreenbelt.com", "http://www.iheartmedia.com", "http://www.jammintogether.com", "http://www.jmoreliving.com", "http://www.kbssportsstrategies.com", "http://www.kentgov.org", "http://www.kentnarrowsmd.com", "http://www.marriott.com", "http://www.maryland.com", "http://www.marylandmotorcoach.org", "http://www.marylandports.com", "http://www.marylandracing.com", "http://www.marylandroadtrips.com", "http://www.marylandsports.us", "http://www.mcdonnellmedia.com", "http://www.mdsoccerplex.org", "http://www.mediaone.digital", "http://www.mediaonena.com", "http://www.medievaltimes.com", "http://www.missshirleys.com", "http://www.ncm.com", "http://www.ocbeachresort.com", "http://www.oceancity.com", "http://www.oceancity.org", "http://www.ocvisitor.com", "http://www.onpointsportsstrategies.com", "http://www.optonline.net", "http://www.orange.com", "http://www.palmergosnell.com", "http://www.phillipsfoods.com", "http://www.platinumpr.com", "http://www.pressboxonline.com", "http://www.princessbayside.com", "http://www.princessroyale.com", "http://www.recreationnews.com", "http://www.rentatour.com", "http://www.rhgcorp.com", "http://www.salisbury.edu", "http://www.seifertassociatesinc.com", "http://www.smcmail.com", "http://www.sojern.com", "http://www.sonesta.com", "http://www.stratosphere.social.com", "http://www.tccsmd.org", "http://www.tdsbrochure.com", "http://www.todaymediacustom.com", "http://www.trade.gov", "http://www.travelspike.com", "http://www.usna.edu", "http://www.visithagerstown.com", "http://www.visitmaryland.org", "http://www.visitstmarysmd.com", "http://www.wandermaps.com", "http://www.whong.media", "http://www.wispresort.com", "http://www.zartico.com"]
    print(f'Scraping the following urls {start_urls}')

    def parse(self, response):
        component_to_xpath_dict = {"h1_tag": "//h1/text()",
                                   "title": "//title/text()",
                                   "meta_description": "//meta[@name='description']/@content",
                                   "image_data": "//img",
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