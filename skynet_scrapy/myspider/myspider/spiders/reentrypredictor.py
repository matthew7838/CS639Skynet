import scrapy
from datetime import date
import calendar
import pandas as pd
from myspider.items import ReentrypredictorItem


class ReentrypredictorSpider(scrapy.Spider):
    name = "reentrypredictor"
    allowed_domains = ["aerospace.org"]
    start_urls = ["https://aerospace.org/reentries/grid?field_reentry_type_target_id%5B%5D=32&field_reentry_sighting_value=All&format_select=table&reentry_timezone_selector=UTC"]

    def parse_limit(self, prediction):
        month_list = []
        month_list_one, month_list_two, month_list_three = ['Jan', 'Feb', 'March', 'Apr'], ['May', 'Jun', 'Jul', 'Aug'], ['Sep', 'Oct','Nov', 'Dec']
        today = date.today()
        curr_month = calendar.month_abbr[today.month]
        curr_year = today.year
        if curr_month in month_list_one and curr_year == int(prediction.css('.views-field-field-predicted-reentry-time .field-data time::text').get().split(' ')[2]):
            month_list = month_list_one[:]
        if curr_month in month_list_two and curr_year == int(prediction.css('.views-field-field-predicted-reentry-time .field-data time::text').get().split(' ')[2]):
            month_list = month_list_two[:]
        if curr_month in month_list_three and curr_year == int(prediction.css('.views-field-field-predicted-reentry-time .field-data time::text').get().split(' ')[2]):
            month_list = month_list_three[:]
        #print(month_list)
        return month_list
        

    def parse(self, response):
        data_list = []
        predictions = response.css('.even')
        odd_predictions = response.css('.odd')
        for odd_prediction in odd_predictions:
            predictions.append(odd_prediction)
        stop_parsing = False

        for prediction in predictions:
            if self.parse_limit(prediction) == []:
                break

            if prediction.css('.views-field-field-predicted-reentry-time .field-data time::text').get().split(' ')[0] not in self.parse_limit(prediction):
                stop_parsing = True
            if prediction.css('.views-field-field-predicted-reentry-time .field-data time::text').get().split(' ')[0] in self.parse_limit(prediction):

                reentrypredictor_item = ReentrypredictorItem()
                reentrypredictor_item['object'] = prediction.css('.views-field-title .field-data a::text').get()
                reentrypredictor_item['mission'] = prediction.css('.views-field-field-mission .field-data::text').get().strip()
                reentrypredictor_item['reentry_type'] = prediction.css('.views-field-field-reentry-type .field-data::text').get().strip()
                reentrypredictor_item['launch_date'] = prediction.css('.views-field-field-launched .field-data time::text').get()
                reentrypredictor_item['predicted_reentry_date'] = prediction.css('.views-field-field-predicted-reentry-time .field-data time::text').get()
                base_url = 'https://aerospace.org/reentries/'
                prediction_url = base_url + prediction.css('.views-field-title .field-data a::text').get().split(" ")[-1].replace(')', '')
                yield scrapy.Request(prediction_url, callback=self.parse_prediction_page, cb_kwargs={'reentrypredictor_item': reentrypredictor_item})

        next_page = response.css('li.pager__item--next a::attr(href)').get()
        print(next_page)
        if next_page is not None and not stop_parsing:
            next_page_url = f'https://aerospace.org/reentries/grid{next_page}'
            print(next_page_url)
            yield response.follow(next_page_url, callback = self.parse)

    def parse_prediction_page(self, response, reentrypredictor_item):
        table_rows = response.css('table tr')
        reentrypredictor_item['norad_num'] = table_rows[7].css('td div::text').get()
        reentrypredictor_item['cospar_num'] = table_rows[6].css('td::text').get()
        yield reentrypredictor_item