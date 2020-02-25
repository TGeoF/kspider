from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from helpers import multiyearSeasonString

season = multiyearSeasonString(2019)
league = '1-bundesliga'
start = 1
recursive = True

process = CrawlerProcess(get_project_settings())
process.crawl('events', season=season,
              league=league, start=start, recursive=recursive)
process.start()
