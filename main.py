from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

process.crawl('MatchSpider', season='2019-20',
              league='1-bundesliga', start=1, recursive=True)
process.start()
