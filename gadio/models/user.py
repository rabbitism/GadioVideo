from gadio.models.asset import Image


class User:

    def __init__(self, user_id, nickname, image_id):
        """Initialize a gadio dj as user

        Arguments:
            nickname {string} -- Nickname of this dj
            avatar_url {string} -- corresponding avatar picture url
        """
        self.user_id = user_id
        self.nickname = nickname
        self.portrait = Image(image_id=image_id, local_name=self.user_id)
        return

    @classmethod
    def load_from_json(cls, parsed_json: str):
        """[summary]
        
        Arguments:
            parsed_json {str} -- json for user
        
        Raises:
            LookupError: Raised when json object is incorrect
            LookupError: Raised when json object is not for initializing user
        
        Returns:
            User -- a instance initialized with json attributes
        """
        try:
            parsed_json['type']
        except:
            raise LookupError('Incorrect json passed to user')

        if parsed_json['type'] != "users":
            raise AttributeError('Json passed to user is not for user')

        try:
            instance = cls(user_id=parsed_json['id'],
                           nickname=parsed_json['attributes']['nickname'],
                           image_id=parsed_json['attributes']['thumb'])
            return instance
        except:
            raise KeyError('Json does not include necessary user attributes')
