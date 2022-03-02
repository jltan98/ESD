import os
from os import environ
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import json
import requests


app = Flask(__name__)
CORS(app)

# Function 1: get all data based on ticker name (identifier)
@app.route("/xignite/<string:search_key>")
def get_all(search_key):
    # url = "https://globalnews.xignite.com/xGlobalNews.json/GetTopSecurityHeadlines?IdentifierType=Symbol&Identifier=" + search_key + "&Count=10&_token=6EB93AA1E310478A962C4198560D4BE9"
    url = "https://globalnews.xignite.com/xGlobalNews.json/GetTopSecurityHeadlines?IdentifierType=Symbol&Identifier={search_key}&Count=10&_token=6EB93AA1E310478A962C4198560D4BE9".format(search_key=search_key)
    data = requests.get(url)
    # return json.loads(data.text)
    if data != "":
        return jsonify(
            {
                "code": 200,
                "data": {
                    "headlines": json.loads(data.text)
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "No data retrieved from Xignite GlobalNews API."
        }
    ), 404

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": calling Xgnite API Top Market Headlines ...")
    app.run(port=5003, debug=True)
