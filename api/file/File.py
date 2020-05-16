
################################################################################

import json

################################################################################

class File:

    data = {}

    def __init__(self, file):
        self.__set_data(file)

    def __set_data(self, file):

        try:
            with open("./" + file, "r") as file:
                self.data = json.load(file)

        except FileNotFoundError:
            print(str(file) + " not found!")
            quit()

################################################################################
