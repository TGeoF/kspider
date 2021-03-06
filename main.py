from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from helpers import multiyearSeasonString

season = multiyearSeasonString(2019)
league = '1-bundesliga'
start = 2
recursive = True

process = CrawlerProcess(get_project_settings())
process.crawl('matches', season=season,
              league=league, start=start, recursive=recursive)
process.start()
