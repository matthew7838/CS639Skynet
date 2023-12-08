from typing import Iterable
import scrapy
from myspider.items import TheSpaceReportItem
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from tqdm import tqdm
from datetime import date, datetime
import pandas as pd
import os
import re
import time

class NanoSatsSpider(scrapy.Spider):

    name = "thespacereportspider"
    # allowed_domains = ["thespacereport.org"]
    start_urls = ["https://www.thespacereport.org/resources/launch-log-2023/"]

    custom_settings = {
        'ITEM_PIPELINES': {
            'myspider.pipelines.TheSpaceReportPipeline': 800,
            },
        'LOG_LEVEL': 'CRITICAL',
    }

    def __init__(self):
        self.scraped_items = list()
        options = Options()
        options.headless = True
        service = Service(executable_path="chromium.chromedriver")
        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options, service=service)

    def parse(self, response):
        url = response.url
        self.driver.get(url)
        time.sleep(1.5)
        table_body = self.driver.find_element(By.TAG_NAME, "tbody")

        # get data from first page and yield element
        for tr in table_body.find_elements(By.TAG_NAME, "tr"):
            thespacereportitem = TheSpaceReportItem()
            tds = tr.find_elements(By.TAG_NAME, "td")
            thespacereportitem["LaunchID"] = tds[0].text
            thespacereportitem["DateTime"] = tds[1].text
            thespacereportitem["LaunchVehicle"] = tds[2].text
            thespacereportitem["OperatorCountry"] = tds[3].text
            thespacereportitem["LaunchSite"] = tds[4].text
            thespacereportitem["Status"] = tds[5].text
            thespacereportitem["MissionSector"] = tds[6].text
            thespacereportitem["Crewed"] = tds[7].text
            thespacereportitem["FirstStageRecovery"] = tds[8].text
            yield thespacereportitem
            self.scraped_items.append(thespacereportitem)
        
        stop = self.driver.find_element(By.ID, "table_3_info")
        condition = re.search(r"([0-9]+) of ([0-9]+)", stop.text)

        while(int(condition[1]) < int(condition[2])):
            # load next set of rows

            next = self.driver.find_element(By.ID, "table_3_next")
            self.driver.execute_script("arguments[0].click();", next)
            time.sleep(1.5)
            table_body = self.driver.find_element(By.TAG_NAME, "tbody")

            for tr in table_body.find_elements(By.TAG_NAME, "tr"):
                thespacereportitem = TheSpaceReportItem()
                tds = tr.find_elements(By.TAG_NAME, "td")
                thespacereportitem["LaunchID"] = tds[0].text
                thespacereportitem["DateTime"] = tds[1].text
                thespacereportitem["LaunchVehicle"] = tds[2].text
                thespacereportitem["OperatorCountry"] = tds[3].text
                thespacereportitem["LaunchSite"] = tds[4].text
                thespacereportitem["Status"] = tds[5].text
                thespacereportitem["MissionSector"] = tds[6].text
                thespacereportitem["Crewed"] = tds[7].text
                thespacereportitem["FirstStageRecovery"] = tds[8].text
                yield thespacereportitem
                self.scraped_items.append(thespacereportitem)

            stop = self.driver.find_element(By.ID, "table_3_info")
            condition = re.search(r"([0-9]+) of ([0-9]+)", stop.text)

    def closed(self, reason):
        self.driver.quit()
        current_datetime = datetime.now().strftime('%m-%d-%Y_%H-%M-%S')
        current_month_year = date.today().strftime('%B_%Y')
        folder_name = os.path.join('CSVs/THESPACEREPORT', current_month_year)
        os.makedirs(folder_name, exist_ok=True)
        csv_filename = os.path.join(folder_name, f'TheSpaceReport_{current_datetime}.csv')
        df = pd.DataFrame(self.scraped_items)
        df.to_csv(csv_filename, index=False)
        print(f'Scraped data exported to {csv_filename}')


    # def start_requests(self):
    #     post_url = 'https://www.thespacereport.org/wp-admin/admin-ajax.php?action=get_wdtable&table_id=257&wdt_var1=2023'
    #     headers = {
    #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    #         "Accept": "application/json, text/javascript, */*; q=0.01",
    #         "Accept-Language": "en-US,en;q=0.5",
    #         "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    #         "X-Requested-With": "XMLHttpRequest",
    #         "Sec-Fetch-Dest": "empty",
    #         "Sec-Fetch-Mode": "cors",
    #         "Sec-Fetch-Site": "same-origin"
    #     }
    #     form_data = {
    #         'draw': '1',
    #         'columns[0][data]': '0',
    #         'columns[0][name]': 'Launch ID',
    #         'columns[0][searchable]': 'true',
    #         'columns[0][orderable]': 'true',
    #         'columns[0][search][value]': '',
    #         'columns[0][search][regex]': 'false',
    #         'columns[1][data]': '1',
    #         'columns[1][name]': 'DateTime',
    #         'columns[1][searchable]': 'true',
    #         'columns[1][orderable]': 'true',
    #         'columns[1][search][value]': '',
    #         'columns[1][search][regex]': 'false',
    #         'columns[2][data]': '2',
    #         'columns[2][name]': 'Launch Vehicle',
    #         'columns[2][searchable]': 'true',
    #         'columns[2][orderable]': 'true',
    #         'columns[2][search][value]': '',
    #         'columns[2][search][regex]': 'false',
    #         'columns[3][data]': '3',
    #         'columns[3][name]': 'Operator Country',
    #         'columns[3][searchable]': 'true',
    #         'columns[3][orderable]': 'true',
    #         'columns[3][search][value]': '',
    #         'columns[3][search][regex]': 'false',
    #         'columns[4][data]': '4',
    #         'columns[4][name]': 'Launch Site',
    #         'columns[4][searchable]': 'true',
    #         'columns[4][orderable]': 'true',
    #         'columns[4][search][value]': '',
    #         'columns[4][search][regex]': 'false',
    #         'columns[5][data]': '5',
    #         'columns[5][name]': 'Status',
    #         'columns[5][searchable]': 'true',
    #         'columns[5][orderable]': 'true',
    #         'columns[5][search][value]': '',
    #         'columns[5][search][regex]': 'false',
    #         'columns[6][data]': '6',
    #         'columns[6][name]': 'Mission Sector',
    #         'columns[6][searchable]': 'true',
    #         'columns[6][orderable]': 'true',
    #         'columns[6][search][value]': '',
    #         'columns[6][search][regex]': 'false',
    #         'columns[7][data]': '7',
    #         'columns[7][name]': 'Crewed',
    #         'columns[7][searchable]': 'true',
    #         'columns[7][orderable]': 'true',
    #         'columns[7][search][value]': '',
    #         'columns[7][search][regex]': 'false',
    #         'columns[8][data]': '8',
    #         'columns[8][name]': 'First Stage Recovery',
    #         'columns[8][searchable]': 'true',
    #         'columns[8][orderable]': 'true',
    #         'columns[8][search][value]': '',
    #         'columns[8][search][regex]': 'false',
    #         'order[0][column]': '1',
    #         'order[0][dir]': 'asc',
    #         'start': '0',
    #         'length': '200',
    #         'search[value]': '',
    #         'search[regex]': 'false',
    #         'wdtNonce': 'c732cba434',
    #     }

    #     yield scrapy.FormRequest()