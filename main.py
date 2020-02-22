from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

season = '2019-20'
league = '1-bundesliga'
start = 1
recursive = True

process = CrawlerProcess(get_project_settings())
process.crawl('matches', season=season,
              league=league, start=start, recursive=recursive)
process.start()
