#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import os

import amqp_setup
import requests

monitorBindingKey='*.success'

def receiveNotification():
    amqp_setup.check_setup()
        
    queue_name = 'Notification'
    
    # set up a consumer and start to wait for coming messages
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 
    #it doesn't exit by default. Use Ctrl+C in the command window to terminate it.

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived a notification by " + __file__)
    processRecommendation(json.loads(body))
    print() # print a new line feed

def processRecommendation(info):
    print(info)
    usertype = info.split(",")[0]

    if (usertype == "client"):
        chat_id = info.split(",")[1]
        investment_id = info.split(",")[2]
        comment = info.split(",")[3]
        bot_token = '1771184288:AAExviJD5YftPmf1vbtuo73DhLCcptyFxz8'
        print("Processing a recommendation:")
        message = "Good day to you, please login to ESD Ventures website to check the updated recommendation, "+investment_id+"."
        if (comment != ""):
            message += " Please note the reason for overwriting the previous recommendation: "+comment+"."
  
    if (usertype == "IC"):
        chat_id = info.split(",")[1]
        investment_id = info.split(",")[2]
        status = info.split(",")[3]
        client_id = info.split(",")[4]
        bot_token = '1672096691:AAE41h_T7jo7S-93QHQt6vmBlg6f_VmQkAk'
        message = "Good day, please note that client ID, "+client_id+" has "+status+" the Investment ID, "+investment_id+"."
        print("Notification Sent")

    telegram_bot_sendtext(message, chat_id, bot_token)

# Telegram Bot API
# Conditions: 
# the person needs to provide the chat ID that is obtainable via IDBot /getid —> needs to be recorded into database. 
# the person needs to start the bot on their telegram to receive the notification
def telegram_bot_sendtext(bot_message, bot_chatID, bot_token):
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveNotification()
