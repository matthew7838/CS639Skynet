import scrapy
import pandas as pd
from io import StringIO
from myspider.items import Planet4589Item

class Planet4589Spider(scrapy.Spider):
    # Define the spider name
    name = "planet4589"
    # Specify the domains allowed to scrape
    allowed_domains = ["planet4589.org"]
    # Specify the initial URL to start scraping from
    start_urls = [ "https://planet4589.org/space/gcat/tsv/cat/satcat.tsv"]

    def parse(self, response):
        # Convert the TSV response into a StringIO object for pandas to read
        tsv_file = StringIO(response.text)
        df = pd.read_csv(tsv_file, sep='\t', dtype=str)
        # Rename the #JCAT column to JCAT
        df.rename(columns={"#JCAT": "JCAT"}, inplace=True)

        # Iterate over the rows of the dataframe
        for _, row in df.iterrows():
            item = Planet4589Item()
            # Populate item fields using DataFrame row values
            for field in item.fields:
                value = row.get(field, '')
                item[field] = str(value).strip()
            # Yield the populated item to further process (by pipelines or feed exports)
            yield item
