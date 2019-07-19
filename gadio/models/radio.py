from gadio.models.asset import Image, Audio
from gadio.models.page import Page
from gadio.models.user import User


class Radio():
    
    def __init__(self):
        self.users = list()
        self.title = ""
        self.radio_id = ""
        self.cover = object()
        self.duration = 0
        self.audio = object()
        self.category = ""
        self.timeline = dict()
        self.timestamps = list()

    @classmethod
    def load_from_json(cls, parsed_json:str):
        #https://www.gcores.com/gapi/v1/radios/112068?include=category,media,djs,media.timelines
        radio = cls()
        radio.radio_id = parsed_json['data']['id']
        radio.title = parsed_json['data']['attributes']['title']
        radio.duration = parsed_json['data']['attributes']['duration']
        radio.cover = Image(parsed_json['data']['attributes']['thumb'], 'cover')

        for item in parsed_json['included']:

            # Set radio category
            if (item['type'] == "categories"):
                radio.category = item['attributes']['name']

            # Set radio audio
            elif (item['type'] == 'medias'):
                radio.audio = Audio(item['attributes']['audio'], radio.radio_id)

            # append radio pages
            elif (item['type'] == 'timelines'):
                page = Page.load_from_json(item['attributes'])
                radio.timeline[page.start_time] = page
                radio.timestamps.append((int)(page.start_time))

            # append radio users
            elif (item['type'] == 'users'):
                user = User.load_from_json(item)
                radio.users.append(user)
            
            else:
                continue
        
        if (0 not in radio.timeline.keys()):
            radio.timestamps.append(0)
        radio.timestamps.append(radio.duration)
        list.sort(radio.timestamps)
        print("Gadio", radio.radio_id, "successfully initialized.")
        print("Title:", radio.title)
        print("Pages:", len(radio.timeline))
        print("Duration:", radio.duration)
        print("DJs:", len(radio.users), [user.nickname for user in radio.users])
        print(radio.timestamps)
