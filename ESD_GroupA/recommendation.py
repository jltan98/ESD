import os
from os import environ
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import json
import requests

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)
CORS(app)


class Recommendation(db.Model):
    __tablename__ = 'recommendation'

    client_id = db.Column(db.Integer, primary_key=True)
    reco_created_date = db.Column(
        db.DateTime, nullable=False, default=datetime.now())
    investment_id = db.Column(db.String(64), nullable=False, primary_key=True)
    ticker_name = db.Column(db.String(64), nullable=False)
    stock_name = db.Column(db.String(1064), nullable=False)
    recommendation = db.Column(db.Text, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    IC_id = db.Column(db.Integer, nullable=False)
    IC_chatid = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(64), nullable=False)

    def __init__(self, client_id, reco_created_date, investment_id, ticker_name, stock_name, recommendation, comment, IC_id, IC_chatid, status):
        self.client_id = client_id
        self.reco_created_date = reco_created_date
        self.investment_id = investment_id
        self.ticker_name = ticker_name
        self.stock_name = stock_name
        self.recommendation = recommendation
        self.comment = comment
        self.IC_id = IC_id
        self.IC_chatid = IC_chatid
        self.status = status

    def json(self):
        return {
            "client_id": self.client_id,
            "reco_created_date": self.reco_created_date,
            "investment_id": self.investment_id,
            "ticker_name": self.ticker_name,
            "stock_name": self.stock_name,
            "recommendation": self.recommendation,
            "comment": self.comment,
            "IC_id": self.IC_id,
            "IC_chatid": self.IC_chatid,
            "status": self.status
        }

# Function 1: to retrieve recommendation for chosen investment of a client


@app.route("/recommendation/<string:client_id>/<string:investment_id>")
def get_recommendation(client_id, investment_id):
    recommendation = Recommendation.query.filter_by(
        client_id=client_id, investment_id=investment_id).first()
    if recommendation:
        return jsonify(
            {
                "code": 200,
                "data": recommendation.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Recommendation not created for this investment.",
        }
    ), 404


# Function 2: Create recommendation
# Receives all attribute values from AskForReco (which compiles UI inputs and retrieves corresponding IC details)
# method is GET for now, need to connect with UI POST request once UI is done. POST will throw "This method is not allowed for the requested URL" error
@app.route("/recommendation", methods=['POST', 'PUT'])
def create_recommendation():
    client_id = request.json.get('client_id', None)
    investment_id = request.json.get('investment_id', None)
    ticker_name = request.json.get('ticker_name', None)
    stock_name = request.json.get('stock_name', None)
    new_recommendation = request.json.get('recommendation')
    comment = request.json.get('comment')
    IC_id = request.json.get('IC_id')
    IC_chatid = request.json.get('IC_chatid')
    reco_created_date = datetime.now()
    status = ""

    # print(reco_created_date)
    recommendation = Recommendation(
        client_id=client_id,
        reco_created_date=reco_created_date,
        investment_id=investment_id,
        ticker_name=ticker_name,
        stock_name=stock_name,
        recommendation=new_recommendation,
        comment = comment,
        IC_id=IC_id,
        IC_chatid=IC_chatid,
        status=status
    )

    # To check if recommendation for this client's investment has already been created
    count = recommendation.query.filter_by(
        client_id=client_id, investment_id=investment_id).count()

    if count == 0:
        try:
            db.session.add(recommendation)
            db.session.commit()

        except Exception as e:
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while creating the recommendation. " + str(e)
                }
            ), 500

        return jsonify(
            {
                "code": 201,
                "data": recommendation.json()
            }
        ), 201
    else:
        recommendation = recommendation.query.filter_by(
            client_id=client_id, investment_id=investment_id).first()
        data = request.get_json()
        if data["recommendation"]:
            recommendation.recommendation = data["recommendation"]
            recommendation.comment = data["comment"]
            recommendation.status = ""
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": recommendation.json()
                }
            ), 200


@app.route("/recommendation/client_update", methods=['POST', 'PUT'])
def updateStatus():
    try:
        client_id = request.json.get('client_id', None)
        investment_id = request.json.get('investment_id', None)
        status = request.json.get('status', None)

        recommendation = Recommendation.query.filter_by(
            client_id=client_id, investment_id=investment_id).first()

        if not recommendation:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "client_id": client_id,
                        "investment_id": investment_id,
                        "status": status
                    },
                    "message": "Recommendation not found."
                }
            ), 404

        data = request.get_json()
        if data['status']:
            recommendation.status = data['status']
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": recommendation.json()
                }
            ), 200

    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "data": {
                    "client_id": client_id,
                    "investment_id": investment_id,
                    "status": status
                },
                "message": "An error occurred while updating the recommendation. " + str(e)
            }
        ), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
