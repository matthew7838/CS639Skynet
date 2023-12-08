from typing import Iterable
import scrapy
from itemadapter import ItemAdapter
from scrapy.http import Request
from myspider.items import NanoSatsItem
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from datetime import date, datetime
import pandas as pd
import os
import re
import io

class NanoSatsSpider(scrapy.Spider):

    name = "nanosatsspider"
    allowed_domains = ["nanosats.eu"]

    custom_settings = {
        'ITEM_PIPELINES': {
            'myspider.pipelines.NanoSatsPipeline': 700,
            },
        'LOG_LEVEL': 'CRITICAL',
    }

    def __init__(self):
        self.scraped_items = list()

    def start_requests(self):
        base_url = "https://www.nanosats.eu/"
        homepage = requests.get('https://www.nanosats.eu/database')
        soup = BeautifulSoup(homepage.text, 'html.parser')
        table = soup.find('table')

        for tr in table.findAll("tr"):
            td = tr.find("td")
            try:
                relative_link = td.find('a')['href'] # maybe only for operational ones after fixing
                link = base_url + relative_link
                # print(link)
                yield Request(link)
            except:
                continue

    def parse(self, response):
        nanosatsitem = NanoSatsItem()
        res = response.text
        df = pd.read_html(io.StringIO(res))[0]

        data = dict()

        # new
        columns = df[0].tolist()
        row = df[1].tolist()

        # new
        for i in range(len(columns)):
            data[columns[i]] = row[i]

        adapter = ItemAdapter(nanosatsitem)
        field_names = adapter.field_names()

        for field_name in field_names:
            adapter[field_name] = data.get(field_name) # none gets converted to null

        # seperate assignment due to name mis-match
        adapter["Units"] = data.get("Units or mass")
        adapter["NORAD"] = data.get("NORAD ID")
        adapter["Launch_Brokerer"] = data.get("Launch brokerer")

        yield nanosatsitem
        self.scraped_items.append(nanosatsitem)        

    def closed(self, reason):
        current_datetime = datetime.now().strftime('%m-%d-%Y_%H-%M-%S')
        current_month_year = date.today().strftime('%B_%Y')
        folder_name = os.path.join('CSVs/NANOSATS', current_month_year)
        os.makedirs(folder_name, exist_ok=True)
        csv_filename = os.path.join(folder_name, f'NanoSats_{current_datetime}.csv')
        df = pd.DataFrame(self.scraped_items)
        df.to_csv(csv_filename, index=False)
        print(f'Scraped data exported to {csv_filename}')
