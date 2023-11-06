from myspider.spiders.orbitalfocusspider import OrbitalfocusspiderSpider
from myspider.spiders.planet4589 import Planet4589spiderSpider
from myspider.spiders.reentrypredictor import ReentrypredictorSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def main():
    spiders = [Planet4589spiderSpider, ReentrypredictorSpider, OrbitalfocusspiderSpider]
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    #process.crawl(OrbitalfocusspiderSpider)
    process.crawl(Planet4589spiderSpider)
    process.crawl(ReentrypredictorSpider)
    process.start()

if __name__ == '__main__':
    main()