import scrapy
import requests
import pandas as pd
from tqdm import tqdm
from myspider.items import UcsdataItem
from io import BytesIO


class UcsdataSpider(scrapy.Spider):
    name = "ucsdataspider"
    allowed_domains = ["ucsusa.org"]
    start_urls = ["https://www.ucsusa.org/resources/satellite-database"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'myspider.pipelines.UcsdataPipeleine': 100,
            },
        'LOG_LEVEL': 'CRITICAL',
    }

    def __init__(self, *args, **kwargs):
        super(UcsdataSpider, self).__init__(*args, **kwargs)
        self.total_count = 0
        self.processed_count = 0
        self.scraped_items = []

    def parse(self, response):
        excel_url = response.css('.column-section .main-region ul li a').attrib['href']
        excel_url = f'https://ucsusa.org{excel_url}'
        print(excel_url)
        response = requests.get(excel_url)
        excel_content = BytesIO(response.content)
        df = pd.read_excel(excel_content)
        df = df.drop(['Comments', 
                      'Unnamed: 28', 
                      'Source Used for Orbital Data',
                      'Source.2',
                      'Source.3',
                      'Source.4',
                      'Source.5',
                      'Source.6',
                      'Unnamed: 37',
                      'Unnamed: 38',
                      'Unnamed: 39',
                      'Unnamed: 40',
                      'Unnamed: 41',
                      'Unnamed: 42',
                      'Unnamed: 43',
                      'Unnamed: 44',
                      'Unnamed: 45',
                      'Unnamed: 46',
                      'Unnamed: 47',
                      'Unnamed: 48',
                      'Unnamed: 49',
                      'Unnamed: 50',
                      'Unnamed: 51',
                      'Unnamed: 52',
                      'Unnamed: 53',
                      'Unnamed: 54',
                      'Unnamed: 55',
                      'Unnamed: 56',
                      'Unnamed: 57',
                      'Unnamed: 58',
                      'Unnamed: 59',
                      'Unnamed: 60',
                      'Unnamed: 61',
                      'Unnamed: 62',
                      'Unnamed: 63',
                      'Unnamed: 64',
                      'Unnamed: 65',
                      'Unnamed: 66',
                      'Unnamed: 67'], axis=1)
        
        column_dic = {
            'Name of Satellite, Alternate Names': 'full_name',
            'Current Official Name of Satellite': 'official_name',
            'Country/Org of UN Registry': 'country',
            'Country of Operator/Owner': 'owner_country',
            'Operator/Owner': 'owner',
            'Users': 'users',
            'Purpose': 'purpose',
            'Detailed Purpose': 'detail_purpose',
            'Class of Orbit': 'orbit_class',
            'Type of Orbit': 'orbit_type',
            'Longitude of GEO (degrees)': 'in_geo',
            'Perigee (km)': 'perigee',
            'Apogee (km)': 'apogee',
            'Eccentricity': 'eccentricity',
            'Inclination (degrees)': 'inclination',
            'Period (minutes)': 'period',
            'Launch Mass (kg.)': 'mass',
            'Dry Mass (kg.)': 'dry_mass',
            'Power (watts)': 'power',
            'Date of Launch': 'launch_date',
            'Expected Lifetime (yrs.)': 'expected_lifetime',
            'Contractor': 'contractor',
            'Country of Contractor': 'contractor_country',
            'Launch Site': 'launch_site',
            'Launch Vehicle': 'launch_vehicle',
            'COSPAR Number': 'cospar',
            'NORAD Number': 'norad',
            'Source': 'source',
            'Source.1': 'additional_source',
        }
        df.rename(columns=column_dic, inplace=True)

        self.total_count = len(df)
        progress_bar = tqdm(total=self.total_count, desc='Latest UCS Excel Scraping Progress', unit='item')

        for index, row in df.iterrows():
            ucs_item = UcsdataItem()
            for field in ucs_item.fields:
                value = row.get(field)
                ucs_item[field] = str(value).strip()
            yield ucs_item
            #print(ucs_item)
            self.processed_count += 1
            self.scraped_items.append(ucs_item)
            progress_bar.update(1)
        progress_bar.close()

    def closed(self, reason):
        if self.total_count > 0:
            percentage_completed = (self.processed_count / self.total_count) * 100
            print(f"Latest UCS Excel Scraping progress: {percentage_completed:.2f}% completed.")