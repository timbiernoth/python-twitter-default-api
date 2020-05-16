
################################################################################

from api.file.File import File
from api.database.Database import Database

################################################################################

class Init:

    config = {}
    database = {}

    def __init__(self, config_file):
        self.__set_config(config_file)
        self.__set_database()

    def __set_config(self, file):
        self.config = File(file)

    def __set_database(self):
        self.database = Database(self.config)

################################################################################
