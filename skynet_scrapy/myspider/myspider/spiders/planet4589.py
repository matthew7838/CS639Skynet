import scrapy
import pandas as pd
from io import StringIO
from myspider.items import Planet4589Item

class Planet4589spiderSpider(scrapy.Spider):
    name = "planet4589spider"
    allowed_domains = ["planet4589.org"]
    start_urls = ["https://planet4589.org/space/gcat/tsv/cat/satcat.tsv"]
    def parse(self, response):
        tsv = StringIO(response.text)
        df = pd.read_csv(tsv, sep='\t', dtype=str)
        df = df.drop(0)
        df.rename(columns={"#JCAT": "JCAT"}, inplace=True)
        df = df[df['LDate'].str.startswith('2023')]
        df = df[df['Status'].str.startswith('O')]
        print(f'length = {len(df)}')
        print(df)
        for index, row in df.iterrows():
            sat_item = Planet4589Item()
            for field in sat_item.fields:
                value = row.get(field)
                sat_item[field] = str(value).strip()
            yield sat_item
