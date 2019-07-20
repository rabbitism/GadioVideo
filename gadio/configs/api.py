"""A list of api or resource url template
"""
api = {
    "audio_url_template": "https://alioss.gcores.com/uploads/audio/{asset}",
    "image_url_template": "https://image.gcores.com/{asset}",
    "radio_api_template": "https://www.gcores.com/gapi/v1/radios/{radio_id}?include=category,media,djs,media.timelines",
    "radio_list_api_template": "https://www.gcores.com/gapi/v1/radios?page[limit]=5&sort=-published-at"
}