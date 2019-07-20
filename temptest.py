from gadio.crawlers.crawler import *
from gadio.models.radio import *
from gadio.media.frame import *
from gadio.media.video import Video

parsed_json = Crawler.crawl(112725)

radio = Radio.load_from_json(parsed_json)
#Crawler.download_assets(radio, 'cache')
#Frame.create_cover(radio)
#Frame.create_page(radio.timeline[radio.timestamps[8]], radio=radio)
Video.create_video(radio)