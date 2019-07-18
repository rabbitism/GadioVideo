from gadio.configs.config import api
import re


class Page():

    def __init__(self, time_stamp, image_identifier, title, content, quote_href):
        """Initialize a page with attributes

        Arguments:
            time_stamp {int} -- starting time of this page, unit: second
            image_url {str} -- image_identifier. Sample: a0bb67be-e44f-4668-a72e-cc487a3f1087.jpeg
            title {str} -- title of this page
            content {str} -- content of this page
            quote_href {str} -- hyperlink to reference of this page, can be empty
        """
        self.time_stamp = time_stamp
        self.title = title
        self.content = content
        self.image_url = set_image_url(image_identifier)
        self.quote_href = quote_href
        self.image_suffix = extract_image_suffix(self.image_url)

    def set_image_url(image_identifier: str):
        """Use image asset identifier to generate image url

        Arguments:
            image_url {str} -- image asset identifier returned by api. Sample: a0bb67be-e44f-4668-a72e-cc487a3f1087.jpeg

        Returns:
            image_url {str} -- image url. Sample: https://image.gcores.com/a0bb67be-e44f-4668-a72e-cc487a3f1087.jpeg
        """
        if ("https://" in image_identifier):
            return image_identifier
        else:
            return api["image_url_template"].format(asset=image_identifier)

    def extract_image_suffix(image_url: str):
        """extract image suffix for accessing local files.

        Arguments:
            image_identifier {str} -- image identifier

        Returns:
            str -- suffix of image(file type). Sample: ".jpg"
        """
        suffix = re.match(".*(\..*)", image_url).group(1)
        return suffix
