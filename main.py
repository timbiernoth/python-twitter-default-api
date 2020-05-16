
################################################################################

from flask import Flask

from api.API import API

################################################################################

api = API("config.json")
api_config = api.config.data
api_output = api.output["json"]

################################################################################

if api_config["output"] == "server":

    app = Flask(__name__)

    @app.route("/")
    def output():
       return api_output

    if __name__ == "__main__":
        app.run()

else:

    print(api_output)

    if api_config["debug"] != False:
        print(api.debug)

################################################################################
