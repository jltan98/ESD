# ESDVentures G4TA
Simple investment enterprise solution created with Flask, Docker, mySQLdb, external APIs

## Installation
- pip install Flask
- pip install Flask-SQLAlchemy
- pip install mysql-connector-python
- pip install requests
- pip install SQLAlchemy
- pip install flask_cors
- python -m pip install pika
- pip install tweepy
- pip install vaderSentiment
- pip install nltk
- pip install pandas
- pip install numpy

## API Setup
====<strong>Telegram Bot API</strong>====
1. Search for two bots, "IC_ESD_Ventures" and "Client_ESDVentures" in Telegram.
2. Type "/start" or click on the link, "/start", to start the two bots.
3. Search for "IDBot" in telegram and click or type "/getid" to retrieve your Telegram's chat ID.
4. Amend the "client_chatid" and "IC_chatid" for any one of the users in the Users database either from the users.sql file or in MySQL phpMyAdmin, using the telegram chat ID retrieved from the "IDBot" in Telegram to set the receiver of the notification.

====<strong>Twitter API</strong>====
- In order to call for twitter's Standard v1.1 API, you would have to sign up for Twitter's developer account. 
- The signup requires users to provide clear elaborations on his/her project where the tweets will be utilised. 
- Do note that it might take some time for Twitter to process the application and applications can be rejected if they do not satisfy Twitter's policies. 
- The keys and tokens and provided, but they belong to ESD G4TA's developer account and hence we strongly advise the user to generate their own. 
1. Navigate to https://developer.twitter.com/en/apply-for-access to sign up for a developer account. 
2. Once the application is accepted, you'll be able to retrieve your personal consumerKey, consumerSecret (key), accessToken as well as accessTokenSecret 
3. Replace the 4 keys (and tokens) in the tweets.py file in line 29 to 32. 

====<strong>Xignite API</strong>====
- In order to call for Xignite's API, you would have to sign up for Xignite's trial account at https://www.xignite.com/xignite-trial.
- The current API token used belongs to ESD G4TA's trial account which will end on 8 April 2021, thus will no longer be usable. 
- If you would like to test it out, after registering for a free trial account in Xignite, please follow the below steps.
1. Navigate to https://www.xignite.com/MyAccount/#/api/tokens to get your API Token or check your registration email that states the activation key which is the API token.
2. Replace the url in the xignite.py file from "...token=6EB93AA1E310478A962C4198560D4BE9" to "...token=[Your API token]".

## Setup Procedures
====<strong>Set-up of docker compose</strong>=====
- Preparation
1. Replace all the [dockerid] in the docker-compose.yml file to your docker ID. 
2. If you are using MAMP or a different mysql port from 3306, you will need to edit the dbURL for "recommendation" and "users" sections of docker-compose.yml to match your connection settings.
3. If you do not have user account, "is213", setup as per Lab 3, then open phpMyAdmin and click on "User accounts" tab. Click "Add User Account" and specify the following:
    User name: (Use text field): is213 ||
    Host name: (Any host): % ||
    Password: (No Password): ||
   Then, under "Global privileges", select "Data", then click "Go" to add the new user account.

- Initialising
1. Open command prompt (CMD window) and change the directory to the respective folder containing the docker-compose.yml file.
2. Run in CMD: *docker-compose up*

- Update image if there are amendments to the codes (if applicable)
1. Open command prompt (CMD window) and change the directory to the respective folder containing the docker-compose.yml file.
2. Run in CMD: *docker-compose down* || To remove the previous containers setup for the app.
3. Run in CMD: *docker image ls* || To view the current docker images build in your docker.
4. Run in CMD: *docker image rm [image id]* || To remove the specific docker image of the file you have edited.
5. Run in CMD: *docker-compose up* ||  Build non-existing docker images that is specified to build in docker-compose.yml and create all the containers for the app.

====<strong>General set-up</strong>====

- Initialising
1. Run WampServer and Docker Desktop to ensure the services are running. 
2. Type *pip freeze* in command prompt and ensure that the listed versions matches the stated versions in the "amqp.reqs.txt" and "http.reqs.txt" requirement files.
3. Save the installed UI folder which consists of the css, js, image and html files into the WAMP www folder.
4. Import the sql files (users.sql and recommendation.sql) into MySQL phpMyAdmin. Note that the recommendation.sql has no inserted data by default, but we have provided 2 test data in the recommendation.sql file, you may use them at your own discretion.

## Navigate application
====<strong>Functionality of app</strong>====
1. Open your browser and enter the localhost URL to the directory that holds the UI folder. By default, the location should be http://localhost/UI/login.html.
2. Select the account type that you wish to test out. For "Investment Counsellor", you may enter the credentials for the first record of Investment Counsellor (IC) in the Users database, [Username: JohnJames, Password: johnjames123]. For "Client", similarly, you may enter the credentials for the first record of Client in the Users database, [Username: JaneAusten, Password: jane_01].
3. <strong>[IC - Home tab]</strong> Upon logging in, you (IC) will be redirected to the Investment UI. On the home page, you may enter the client_id in the input field/search bar and click on search to view the client and their investment details that you are in-charge of. If you using the specified credentials for John James, then the client_id value will be 1. Upon successful search, the client and investment details will be displayed. You may click on the "Recommend" button under the "Make Recommendation" column to make recommendation for the client you are in charge of. Please select the investment_id that you are interested to make recommendation for, then input your recommendation in the textarea box. Once done, you may click on the submit button. You should receive an alert that states that the recommendation has been successfully updated. Around the same time, you (as a client) should receive a notification from the "Client_ESDVentures" bot, stating a message to login to check the updated recommendation for a specific investment id.
4. <strong>[IC - Twitter tab]</strong> Input in a search keyword in the input field/search bar and click search to view the public sentiments on tweets relating to the keyword. The sentiment value for "positive" is highlighted in green, and for "negative", it is highlighted in red. 
5. <strong>[IC - News tab]</strong> Input in a company identifier (ticker_name) in the input field/search bar and click on search to view the top 10 security headline news and summary relating to the ticker input.
6. <strong>[IC - Recommendation Status tab]</strong> A dropdown box is shown where you may select the investment ID that client is interested in to view the details of the recommendation made and its current status.
7. <strong>[Client - Home tab]</strong> A dropdown box is shown where you (client) may select the investment ID that you are interested in and view the details of the recommendation made and its current status. If the current status is pending, an option is available under the "Choose Recommendation" column where you can either select "Approve" or "Reject" button. Upon selection, the status will be updated to the choice you have made e.g. You have already approved this recommendation. Around the same time, you should receive a notification from "IC_ESD_Ventures bot", stating a message that a specific client has either approve or reject the specific investment that IC had made recommendation for. 
8. <strong>[Client - Contact Us tab]</strong> If there is further clarification required with the IC, you may either call the support by manually dial or click on the link stating the number, or you can click on the email address link to send an email to ESDVentures. An address is also provided if you wishes to have a face to face discussion.
9. By clicking on the icon beside your name on the top right hand corner, there will be a dropdown option to logout of your account. The session details will be reset and you will be redirected back to the login page.

====<strong>Error Handling</strong>====
1. <strong>[Login page]</strong> If you did not select an account type, an alert will pop up requesting you to select an account type. If you input wrong credentials, a warning message will show up stating the number of attempts left. If you max out your attempts, the fields are disabled.
2. <strong>[Login page]</strong> All sessions start from the login page. If you access for example the 'investment.html' page without logging in, you will be redirect to the login page for verification. 
3. <strong>[Login page]</strong> After logging out, if you click on the back-button to attempt to re-enter into the previously accessed page, it will not work. Vice versa, when you have logged into the system, even if you click on the back-button, you will not be able to go back into the login page. In addition, when you are in the session, even if you change the URL to access into the login page, it will redirect back to the home page of your respective UI (Client - client_recommendation.html, IC - investment.html). You are also unable to change the URL to access into the UI of the other user_type (e.g. if you are IC, you cannot access client UI; vice versa). The session will only end either when you close the web browser or click on logout. 
4. <strong>[IC - Home tab]</strong> If you search for client_id that you are NOT in-charge of, it will display a message stating that you are not be authorised to view this client. This is created for confidentiality purposes. Also, if the client_id does not exist in the Users database, a message will be displayed that client ID is not found. 
5. <strong>[IC - Home tab - Recommendation modal]</strong> If you submit an empty field recommendation, an alert message will pop up asking to input recommendation before submitting. If you checked the box stating that you wish to overwrite the previous approved recommendation, you must enter a comment stating the reason, else, an alert will pop up asking to state the reason for overwriting before proceeding.
6. <strong>[For IC - Twitter tab]</strong> If you input a keyword that is not found from Twitter API, it will display a message stating "[search_key] not found. Please try another keyword."
7. <strong>[For IC - News tab]</strong> If you input a identifier not found from Xignite API, a message stating "[search_key] not found. Please try another company identifier" is displayed.
8. <strong>[IC - Recommendation Status tab]</strong> If the recommendation has yet to be made (does not exist in Recommendation database), a message will be displayed stating "Recommendation not created for this investment". If there is no data retrieved, the default message is "There is a problem retrieving investment data, please try again later.".
9. <strong>[Client - Home tab]</strong> If the recommendation has yet to be made (does not exist in Recommendation database), a message will be displayed stating "Recommendation not created for this investment". If there is no data retrieved, the default message is "There is a problem retrieving investment data, please try again later.".

## Overview video of our app functionalities and navigation
- https://youtu.be/P0QeLGXqCMI

## General Information on (micro)services
1. Users: Retrieve all or specific Investment Counsellor (IC) and Client's information.
2. Recommendation: Retrieve recommendation for specific investment, create recommendation for client's investment and update the status of a particular recommendation.
3. Tweets: Retrieve tweets relating to search_key from Twitter API with analysed sentiment value ("Positive", "Neutral", "Negative").
4. Xignite: Retrieve security headline news and summary relating to company identifier from Xignite API.
5. Notification: Sends a message to notify Investment Counsellor or Client on the investment update on recommendation through Telegram Bot API.
6. Make Recommendation: Invokes Recommendation to create recommendation and invokes Users microservice to request client information. Then sends the relevant information to the notification service via amqp through RabbitMQ (message broker).
7. Validate Recommendation: Invokes Recommendation to update recommendation status and invokes Users microservice to request Investment Counsellor's telegram chat ID. Then sends the relevant information to the notification service via amqp through RabbitMQ (message broker).
