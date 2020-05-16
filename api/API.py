
################################################################################

from api.Init import Init
from apps.TwitterDefaultApp import TwitterDefaultApp
from api.Data import Data

################################################################################

class API:

    debug = ""
    config = {}
    output = {}

    _data = {}
    _database = {}

    def __init__(self, config_file):
        setup = Init(config_file)
        self.config = setup.config
        self._database = setup.database
        self.__run()

    def __run(self):
        self.__set_data()
        self.__close_db()
        self.__set_output()
        self.__set_output_debug()

    def __get_output_debug_loop(self, data):

        output = "\n-------\n\n"

        for name, commands in data.items():
            output = output + name + ":\n"

            for command in commands:
                output = output + "\n" + str(command)

            output = output + "\n\n-------\n\n"

        return output


    def __get_output_debug(self):
        debug_data = self.output["raw"]["data"]["debug"]
        return self.__get_output_debug_loop(debug_data)

    def __set_data(self):
        self._data = Data(self.config, self._database, {
            "twitter": {
                "default": TwitterDefaultApp(self.config, self._database)
            }
        });

    def __set_output(self):
        self.output = self._data.output

    def __set_output_debug(self):
        self.debug = self.__get_output_debug()

    def __close_db(self):

        try:
            self._database.close()
            if self.config.data["debug"] != False:
                print("\n-------\n")

        except NameError:
            print(self.config.data["messages"]["database_object_not_found"])
            quit()

################################################################################
