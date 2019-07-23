from gadio.crawlers.crawler import Crawler
from gadio.models.radio import Radio
import sys

import os

if __name__ == "__main__":
    parsed_json = object
    if (len(sys.argv) == 1 or sys.argv[1]=='-t'):
        print("----------")
        print("Start to create the latest gadio video...")
        id = Crawler.get_latest()
        print(id)
        parsed_json = Crawler.crawl(id)
    else:
        radio_id = int(sys.argv[1])
        parsed_json = Crawler.crawl(radio_id)
    radio = Radio.load_from_json(parsed_json)
    Crawler.get_headers(radio)
    if (len(sys.argv) >= 2):
        if ('-t' in sys.argv):
            {}
        else:
            Crawler.download_assets(radio, os.curdir+os.sep+'cache')
