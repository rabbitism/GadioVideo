class User():

    def __init__(self, nickname, avatar_url):
        """Initialize a gadio dj as user
        
        Arguments:
            nickname {string} -- Nickname of this dj
            avatar_url {string} -- corresponding avatar picture url
        """
        self.nickname = nickname
        self.avatar_url = avatar_url
        return