
################################################################################

import json

################################################################################

class Data:

    output = {}

    _db = {}
    _input = {}
    _config = {}

    _data = {
        "data": {
            "apis": {
                "data": {
                    "twitter": {
                        "default": {
                            "users": [],
                            "tweets": []
                        }
                    }
                }
            },
            "debug": {
                "db_queries": [],
                "api_methods": []
            }
        }
    }

    _apps = {
        "twitter": {
            "default": {}
        }
    }

    def __init__(self, config, db, input):
        self._config = config.data
        self._db = db
        self._input = input
        self.__run()

    def __run(self):
        self.__set_data_twitter_default()
        self.__set_data_debug()
        self.__set_output()

    def __set_output(self):
        json_string = json.dumps(self._data["data"]["apis"])
        json_data = json.loads(json_string)
        self.output = {
            "raw": self._data,
            "json": json_data
        }

    def __set_data_twitter_default(self):

        input = self._input["twitter"]["default"]
        db_tables = self._config["database"]["tables"]["apis"]["twitter"]["default"]

        twitter_users = input.data["users"]
        if input.is_updated_data != False:
            twitter_users = self._db.select("*", db_tables["users"])

        for data in twitter_users:
            data.update({"last_checked_at": int(data["last_checked_at"].timestamp())})
            self._data["data"]["apis"]["data"]["twitter"]["default"]["users"].append(data)

        twitter_tweets = input.data["tweets"]
        if input.is_updated_data != False:
            twitter_tweets = self._db.select("*", db_tables["tweets"])

        for data in twitter_tweets:
            data.update({"created_at": int(data["created_at"].timestamp())})
            data.update({"last_checked_at": int(data["last_checked_at"].timestamp())})
            self._data["data"]["apis"]["data"]["twitter"]["default"]["tweets"].append(data)

    def __set_data_debug(self):
        self._data["data"]["debug"]["db_queries"] = self._db.queries
        self._data["data"]["debug"]["api_methods"] = self._input["twitter"]["default"].api_methods

################################################################################
