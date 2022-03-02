from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json


# map (email obtained from) recommendation micro -> Notification_topic exchange  ->Notification queue -> Notification micro

app = Flask(__name__)
CORS(app)

####need change according to the respective microservices
users_URL = environ.get('users_URL') or "http://localhost:5000/users/ic_chatid"
recommendation_URL = environ.get('recommendation_URL') or "http://localhost:5001/recommendation/client_update"

#function to check requested data is json
@app.route("/validate_recommendation", methods=['POST']) # Routing URL for complex microservice 
def validate_recommendation():
    # Simple check of input format and data of the request are JSON
    if request.is_json:
        try:
            recommendation = request.get_json() #if the created status is json
            print("\nReceived validation of recommendation in JSON:", recommendation)

            # do the actual work
            # 1. Send in recommendation list {recommendation_list}
            result = recoStatus(recommendation)
            print('\n------------------------')
            print('\nresult: ', result)
            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "validate_recommendation.py internal error: " + ex_str
            }), 500

    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def recoStatus(recommendation):
    # Send to notification.py to notify IC on the status process
    print('\n-----Invoking recommendation microservice-----')
    recommendation_output = invoke_http(recommendation_URL, method='PUT', json=recommendation)
    print('Recommendation:', recommendation_output)
   
    code = recommendation_output['code']
    client_id = recommendation_output["data"]["client_id"]
    data = recommendation_output["data"]

    if code in range(200,300):  
        chat_id = processUsers(client_id)
        info_str = "IC,"+str(chat_id)+","+data["investment_id"]+","+data["status"]+","+str(data["client_id"])
        info_json = json.dumps(info_str)
        
            # 4. record new status to notification queue
            #print('\n\n-----Invoking notification microservice-----')
        print('\n\n-----Publishing the (submission) message with routing_key=status.success-----')        

        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="status.success", 
                body=info_json)
        
        print("\nRecommendation published to RabbitMQ Exchange.\n")
        # - reply from the invocation is not used;
        # continue even if this invocation fails

        return {
            "code": 201,
            "data": {
                "recommendation_output": recommendation_output,
            }
        }
    else:
        return {
            "code": 400,
            "data": {
                "recommendation_output": "Failed to get the status of recommendation"
            }
        }
        
# GET Chat_ID from users URLs
def processUsers(client_id):
    # print(client_id)
    print('\n-----Invoking users microservice-----')
    IC_chatid= invoke_http(users_URL+"/"+str(client_id), method='GET')
    IC_chatid = IC_chatid["data"]["IC_chatid"]
    print('IC_chatid:', IC_chatid)

    return IC_chatid


# Execute this program if it is run as a main script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for status of recommendation...")
    app.run(host="0.0.0.0", port=5200, debug=True)
    # Notes for the parameters: 
    # - debug=True will reload the program automatically if a change is detected;
    #   -- it in fact starts two instances of the same flask program, and uses one of the instances to monitor the program changes;
    # - host="0.0.0.0" allows the flask program to accept requests sent from any IP/host (in addition to localhost),
    #   -- i.e., it gives permissions to hosts with any IP to access the flask program,
    #   -- as long as the hosts can already reach the machine running the flask program along the network;
    #   -- it doesn't mean to use http://0.0.0.0 to access the flask program.
