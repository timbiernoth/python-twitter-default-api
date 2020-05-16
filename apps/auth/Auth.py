
################################################################################

import requests
import requests_oauthlib

import twitter

################################################################################

class Auth:

    api_methods = []

    twitter = {}

    _config = {}

    def __init__(self, config):
        self.__set_config(config)
        self.__set_twitter()

    def __set_twitter(self):

        api = self._config["apis"]["twitter"]["default"]
        keys = api["keys"]

        self.twitter = twitter.Api(
            consumer_key = keys["consumer_key"],
            consumer_secret = keys["consumer_secret"],
            access_token_key = keys["access_token_key"],
            access_token_secret = keys["access_token_secret"],
            tweet_mode = keys["tweet_mode"]
        )

        self.api_methods.append(("TwitterDefaultApp", "Auth"))

    def __set_config(self, config):
        self._config = config

################################################################################
