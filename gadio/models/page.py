from gadio.configs.api import api
from gadio.text import text as text
from gadio.models.asset import Image


class Page():

    def __init__(self, start_time, image_id, title, content, quote_href):
        """Initialize a page with attributes

        Arguments:

            time_stamp {int} -- starting time of this page, unit: second

            image_identifier {str} -- Sample: a0bb67be-e44f-4668-a72e-cc487a3f1087.jpeg

            title {str} -- title of this page

            content {str} -- content of this page

            quote_href {str} -- hyperlink to reference of this page, can be empty

        """
        self.start_time = start_time
        self.title = title
        self.content = content
        self.quote_href = quote_href
        self.image = Image(image_id=image_id, local_name = self.start_time)

    @classmethod
    def load_from_json(cls, attributes: dict):
        try:
            page = cls(start_time=attributes['at'],
                       image_id=attributes['asset'],
                       title=attributes['title'],
                       content=attributes['content'],
                       quote_href=attributes['quote-href'])
            return page
        except:
            raise LookupError(
                "Incorrect JSON format. Please check API for update.")
