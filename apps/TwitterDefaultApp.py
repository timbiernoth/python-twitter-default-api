
################################################################################

from datetime import datetime

from apps.auth.Auth import Auth

################################################################################

class TwitterDefaultApp:

    is_updated_data = False

    api_methods = []

    data = {
        "users": {},
        "tweets": {}
    }

    _api = {}
    _db = {}

    _users = {}
    _tweets = {}

    _config = {
        "api": {},
        "db_tables": {}
    }

    def __init__(self, config, db):

        api = Auth(config.data)
        for auth_api_method in api.api_methods:
            self.api_methods.append(auth_api_method)

        self._api = api.twitter
        self._db = db
        self.__set_config(config)
        self.__run()

    def __run(self):
        self.__set_data()
        self.__set_users()
        self.__set_tweets()
        self.__store_users()
        self.__store_tweets()

    def __store_users(self):

        for user, data in self._users.items():

            user_id = ("twitter_users_id", data["id"])
            user_data = [
                user_id,
                ("name", data["name"].strip()),
                ("screen_name", data["screen_name"]),
                ("location", data["location"].strip()),
                ("verified", data["verified"]),
                ("favourites_count", data["favourites_count"]),
                ("followers_count", data["followers_count"]),
                ("friends_count", data["friends_count"]),
                ("listed_count", data["listed_count"]),
                ("statuses_count", data["statuses_count"]),
                ("last_checked_at", datetime.now())
            ]

            check_user = self._db.check_entries(("twitter_users_id", user_id), self.data["users"], user_data)

            if "exists" in check_user:
                if "is_not_up_to_date" in check_user:
                    self.is_updated_data = True
                    self._db.update(self._config["db_tables"]["users"], user_data, [user_id])
            else:
                self.is_updated_data = True
                self._db.insert(self._config["db_tables"]["users"], user_data)

    def __store_tweets(self):

        for user, user_data in self._users.items():

            for tweet in self._tweets[user]:

                tweet_id = ("twitter_tweets_id", tweet.id)
                tweet_data = [
                    tweet_id,
                    ("twitter_users_id", user_data["id"]),
                    ("created_at", datetime.strptime(tweet.created_at,'%a %b %d %H:%M:%S +0000 %Y')),
                    ("lang", tweet.lang.strip()),
                    ("full_text", tweet.full_text.strip()),
                    ("favorite_count", tweet.favorite_count),
                    ("retweet_count", tweet.retweet_count),
                    ("retweeted", tweet.retweeted),
                    ("last_checked_at", datetime.now())
                ]

                check_tweet = self._db.check_entries(("twitter_tweets_id", tweet_id), self.data["tweets"], tweet_data)

                if "exists" in check_tweet:
                    if "is_not_up_to_date" in check_tweet:
                        self.is_updated_data = True
                        self._db.update(self._config["db_tables"]["tweets"], tweet_data, [tweet_id])
                else:
                    self.is_updated_data = True
                    self._db.insert(self._config["db_tables"]["tweets"], tweet_data)

    def __get_users(self):
        users = {}
        for user in self._config["api"]["sources"]["users"]:
            users[user] = self._api.GetUser(screen_name = user, return_json = self._config["api"]["return_json"])
            self.api_methods.append(("TwitterDefaultApp", "GetUser: " + str(user)))
        return users

    def __get_tweets(self):
        tweets = {}
        for user in self._config["api"]["sources"]["users"]:
            tweets[user] = self._api.GetUserTimeline(screen_name = user, count = self._config["api"]["timeline_count"])
            self.api_methods.append(("TwitterDefaultApp", "GetUserTimeline: " + str(user)))
        return tweets

    def __set_users(self):
        self._users = self.__get_users()

    def __set_tweets(self):
        self._tweets = self.__get_tweets()

    def __set_data(self):
        self.data["users"] = self._db.select("*", self._config["db_tables"]["users"])
        self.data["tweets"] = self._db.select("*", self._config["db_tables"]["tweets"])

    def __set_config(self, config):
        self._config = {
            "api": config.data["apis"]["twitter"]["default"],
            "db_tables": config.data["database"]["tables"]["apis"]["twitter"]["default"]
        }

################################################################################
