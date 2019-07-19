from gadio.crawlers.crawler import *
from gadio.models.radio import *

parsed_json = Crawler.crawl(112725)

Radio.load_from_json(parsed_json)