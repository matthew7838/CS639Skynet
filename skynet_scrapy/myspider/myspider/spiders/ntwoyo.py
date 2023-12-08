from typing import Iterable
import scrapy
from scrapy.http import Request
from myspider.items import NtwoYOItem
from tqdm import tqdm
from datetime import date, datetime
import pandas as pd
import os
import psycopg2
import re

class NtwoYOSpider(scrapy.Spider):
 
    name = "ntwoyospider"
    allowed_domains = ["n2yo.com"]
    
    custom_settings = {
        'ITEM_PIPELINES': {
            'myspider.pipelines.NtwoYOPipeline': 600,
            },
        'LOG_LEVEL': 'CRITICAL',
    }
 
    def __init__(self):
        self.scraped_items = list()
        hostname = 'localhost'
        username = 'skynetapp'
        password = 'skynet'
        # database = 'skynetapp' # not necessary
        # port = 5432 # using default
        
        self.connection = psycopg2.connect(host=hostname, user=username, password=password)
        self.cur = self.connection.cursor()

    def start_requests(self):
        self.cur.execute("SELECT Satcat FROM planet4589")
        base_url = "https://www.n2yo.com/satellite/?s="

        for norad in self.cur:
            url = base_url + str(norad[0])
            # print(url)
            yield Request(url)

    def parse(self, response):
        ntwoyoitem = NtwoYOItem()
        res = response.text
        ntwoyoitem["NORAD"] = re.search(r"=([0-9]+)", response.request.url)[1]
        period = re.search(r"Period.+?([0-9]+\.[0-9]+)", res)
        
        if period == None:
            # ntwoyoitem["Period"] = "NULL"
            ntwoyoitem["Period"] = None
        else:
            ntwoyoitem["Period"] = period[1]
            # print(period[1])

        yield ntwoyoitem
        self.scraped_items.append(ntwoyoitem)
        
    def closed(self, reason):
        self.cur.close()
        self.connection.close()
        current_datetime = datetime.now().strftime('%m-%d-%Y_%H-%M-%S')
        current_month_year = date.today().strftime('%B_%Y')
        folder_name = os.path.join('CSVs/N2YO', current_month_year)
        os.makedirs(folder_name, exist_ok=True)
        csv_filename = os.path.join(folder_name, f'N2YO_{current_datetime}.csv')
        df = pd.DataFrame(self.scraped_items)
        # print(df)
        df.to_csv(csv_filename, index=False)
        print(f'Scraped data exported to {csv_filename}')