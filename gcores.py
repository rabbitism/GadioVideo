from gadio.crawlers.crawler import *
from gadio.media.video import *
from gadio.text.text import *


def main(id: int, skip_crawling: bool, with_quote: bool):
    parsed_json = Crawler.crawl(id)
    cache_dir = os.sep.join([os.curdir, 'cache', str(id)])
    data_json = os.sep.join([cache_dir, 'data.json'])
    with open(data_json, 'r', encoding='utf-8'):
        radio = Radio.load_from_json(parsed_json)
        if not skip_crawling:
            Crawler.download_assets(radio, os.curdir + os.sep + 'cache', with_quote)
        Video.create_video(radio)


if __name__ == "__main__":
    skip_crawling = False
    with_quote = False
    if len(sys.argv) == 1 or sys.argv[1] == '-s' or sys.argv[1] == '-q':
        if "-q" in sys.argv:
            with_quote = True
        print("----------")
        print("Start to create the latest gadio video...")
        id = Crawler.get_latest()
        print(id)
        main(id, False, with_quote)
    else:
        title = sys.argv[1]
        skip_crawling = False
        if len(sys.argv) > 2:
            if "-s" in sys.argv:
                skip_crawling = True
            elif "-q" in sys.argv:
                with_quote = True

        if title.endswith(".txt"):
            # 根据下载列表逐个下载
            id_list_file = open(title, "r")
            lines = id_list_file.readlines()
            for line in lines:
                id = int(line)
                main(id, skip_crawling, with_quote)
        else:
            main(int(title), skip_crawling, with_quote)
