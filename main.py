from gadio.crawlers.crawler import *
from gadio.models.radio import *
from gadio.media.video import *
from gadio.text.text import *
import sys

def main(id: int, skip_crawling: bool):
    parsed_json = Crawler.crawl(id)
    cache_dir = os.sep.join([os.curdir, 'cache', str(id), 'data.json'])
    with open(cache_dir, 'r', encoding='utf-8') as file:
        radio = Radio.load_from_json(parsed_json)
        if (not skip_crawling):
            Crawler.download_assets(radio, os.curdir+os.sep+'cache')
        Video.create_video(radio)

if __name__ == "__main__":
    skip_crawling = False
    if (len(sys.argv) == 1 or sys.argv[1]=='-s'):
        print("----------")
        print("Start to create the latest gadio video...")
        id = Crawler.get_latest()
        print(id)
        main(id, False)
    else:
        title = sys.argv[1]
        skip_crawling = False
        if (len(sys.argv) > 2):
            if ("-s" in sys.argv):
                skip_crawling = True
        main(int(title), skip_crawling)


