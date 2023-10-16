# Introdcution
We are great Skynet team

## Technology Stack
Language: Python

Web crawler: Scrapy

### myspider
A crawler program written based on the Scrapy framework for scraping data from websites.

All crawler files are stored in the **spiders** folder.

To use the crawler, please configure the environment correctly
``` python
pip install scrapy # install scrapy

cd myspider # Make sure you in target file
scrapy genspider spidername example.com # You can use this command to create new crawler

scrapy crawl planet4589  # (run crawler name "planet4589")

scrapy crawl planet4589 -o filename.csv # (export data to filename.csv)


```
