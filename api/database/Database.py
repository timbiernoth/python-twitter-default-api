
################################################################################

import html
from datetime import datetime

import psycopg2
from psycopg2 import Error

################################################################################

class Database:

    queries = []

    _config = {}

    __connection = {}
    __cursor = {}

    def __init__(self, config):
        self.__set_config(config)
        self.__set_connection()
        self.__set_cursor()

    def _query(self, query, echo = False): # NOT ALLOWED from extern!!! SECURITY!!!

        query = query.strip()

        self.queries.append(query)
        self.__cursor.execute(query)

        if query.lower().startswith('select '):

            names = []
            i = 0
            for description in self.__cursor.description:
                names.append(self.__cursor.description[i][0])
                i = i + 1

            output = []
            for data in self.__cursor.fetchall():
                key_values = {}
                i = 0
                for value in data:
                    key_values[names[i]] = value
                    i = i + 1
                output.append(key_values)

            if echo:
                print(output)
            else:
                return output

        else:
            self.__connection.commit()

    def select(self, select = "*", table = "", where = [], extend = ""): # GET

        query = "SELECT " + select + " FROM " + table

        if where:
            query = query + self.__get_loop_string(where, "WHERE", "AND")

        query = query + " " + extend + ";"

        return self._query(query)

    def insert(self, table = "", input = [], extend = ""): # POST

        data = {
            "columns": [],
            "values": []
        }

        for name, value in input:
            data["columns"].append(name)
            data["values"].append("'" + self.__escape_string(str(value)) + "'")

        query = "INSERT INTO " + table + " (" + ", ".join(data["columns"]) + ") VALUES (" + ", ".join(data["values"]) + ") " + extend + ";"

        self._query(query)

    def update(self, table = [], set = [], where = [], extend = ""): # PUT

        query = "UPDATE " + table

        if set:
            query = query + self.__get_loop_string(set, "SET", ",")

        if where:
            query = query + self.__get_loop_string(where, "WHERE", "AND")

        query = query + " " + extend + ";"

        self._query(query)

    def delete(self, table = "", where = [], extend = ""): # DELETE

        query = "DELETE FROM " + table

        if where:
            query = query + self.__get_loop_string(where, "WHERE", "AND")

        query = query + " " + extend + ";"

        self._query(query)

    def close(self):

        if self.__connection:
            self.__cursor.close()
            self.__connection.close()
            if self._config["debug"] != False:
                print(self._config["messages"]["database_connection_is_closed"])

    def check_entries(self, by, is_entries, do_entries):

        status = []

        for is_entry in is_entries:

            if str(is_entry[by[0]]) == str(by[1][1]):

                status.append("exists")

                for do_name, do_value in do_entries:

                    time_interval = 0
                    if do_name == "last_checked_at":
                        time_interval = int(do_value.timestamp()) - int(is_entry[do_name].timestamp())

                    if str(is_entry[do_name]) != str(do_value) and time_interval >= self._config["database"]["update_interval"]:
                        status.append("is_not_up_to_date")
            else:
                status.append("not_exists")

        return status

    def __get_loop_string(self, data = [], clause = "", separator = ""):

        string = " " + clause + " "

        i = 1
        for name, value in data:

            string = string + name + "='" + self.__escape_string(str(value)) + "'"
            if i != len(data):
                string = string + " " + separator + " "

            i = i + 1

        return string

    def __escape_string(self, string):
        return html.escape(string)

    def __set_connection(self):

        try:
            self.__connection = psycopg2.connect(
                user = self._config["database"]["user"],
                password = self._config["database"]["password"],
                database = self._config["database"]["database"],
                host = self._config["database"]["host"],
                port = self._config["database"]["port"]
            )

        except (Exception, psycopg2.Error) as error:
            print(self._config["messages"]["error_while_connecting_to_database"], error)
            quit()

    def __set_cursor(self):
        self.__cursor = self.__connection.cursor()

    def __set_config(self, config):
        self._config = config.data


################################################################################
