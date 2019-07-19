from gadio.crawlers.crawler import *
from gadio.models.radio import *

parsed_json = Crawler.crawl(112725)

radio = Radio.load_from_json(parsed_json)
Crawler.download_assets(radio, 'cache')