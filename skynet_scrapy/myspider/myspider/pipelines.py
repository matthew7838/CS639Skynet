# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd


class Planet4589FilterPipeline:
    def __init__(self):
        self.processed_items = []

    def close_spider(self, spider):
        df = pd.DataFrame(self.processed_items)
        df.to_csv('test.csv', sep=',', index=False, header=True)

    def process_item(self, item, spider):
        df = pd.DataFrame([item])

        # Apply the filter
        pattern = r'\bdeb\b|\bdebris\b|\bRemoveDebris\b|DebrisSat'

        mask_bus = df['Bus'].str.contains(pattern, case=False, regex=True, na=False)
        mask_name = df['Name'].str.contains(pattern, case=False, regex=True, na=False)
        mask_plname = df['PLName'].str.contains(pattern, case=False, regex=True, na=False)

        # Combine the individual masks
        combined_mask = mask_bus | mask_name | mask_plname

        df = df[~combined_mask]

        if df.empty:
            return None  # Drop the item
        else:
            # Append the item to the CSV
            processed_item = df.iloc[0].to_dict()
            self.processed_items.append(processed_item)
            return processed_item

