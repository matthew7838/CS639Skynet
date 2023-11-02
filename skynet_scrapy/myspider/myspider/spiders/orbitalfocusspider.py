import scrapy
from myspider.items import OrbitalfocusItem

class OrbitalfocusspiderSpider(scrapy.Spider):
    name = "orbitalfocusspider"
    allowed_domains = ["orbitalfocus.uk"]
    start_urls = ["http://orbitalfocus.uk/Diaries/Launches/Decays.php"]
    

    def parse(self, response):
        satellites = response.css('center')[3].css('.bodyrow')
        for satellite in satellites:
            orbitalfocus_item = OrbitalfocusItem()
            #NORAD Number
            orbitalfocus_item['cat_no'] = satellite.css('td::text')[0].get()
            #COSPAR Number
            orbitalfocus_item['designation'] = satellite.css('td::text')[1].get()
            orbitalfocus_item['name'] = satellite.css('td strong::text')[0].get()
            orbitalfocus_item['date'] = satellite.css('td strong::text')[1].get()
            yield orbitalfocus_item