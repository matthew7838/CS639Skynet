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
import psycopg2
import logging


class TheSpaceReportSpider(scrapy.Spider):

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

        ### path to chromedriver
        ### 1. either have an executable in the same directory as in the next line
        #service = Service(executable_path="chromedriver")
        ### 2. or place the executable in your path as in the next line
        service = Service(executable_path="chromium.chromedriver")

        options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options, service=service)

    def parse(self, response):
        url = response.url
        self.driver.get(url)
        time.sleep(1.5)

        table_body = self.driver.find_element(By.TAG_NAME, "tbody")
        condition = True

        while(condition):

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
            temp = re.search(r"([0-9]+) of ([0-9]+)", stop.text)
            condition = int(temp[1]) < int(temp[2])

            next = self.driver.find_element(By.ID, "table_3_next")
            self.driver.execute_script("arguments[0].click();", next)
            time.sleep(1.5)


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
