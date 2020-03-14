# /index.py
from flask import Flask, request, jsonify, render_template, redirect
import os
import dialogflow_v2 as dialogflow
import requests
import json
import pusher
from werkzeug.utils import secure_filename
from trim import song
from therapy import find
from sendemail import sendmail
from video_emotion import output
import cv2
import imutils
import cv2
from tensorflow import keras
import numpy as np
import time

app = Flask(__name__)
lol = 0


@app.route('/chatbot_page')
def chatbot_page():
    return render_template('index.html')


@app.route('/tictac')
def tictac():
    return render_template("tictac.html")


@app.route("/webcam")
def webcam():
    return render_template('webcam.html')


@app.route("/extras")
def extras():
    return render_template("extra.html")


@app.route('/predict2', methods=['GET'])
def predict2():

    global lol
    file_path = "D:\Downloads\screenshot.jpg"
    fin, mood = output(file_path)

    os.remove(file_path)
    # cv2.imshow("image", fin)
    # cv2.waitKey(0)
    new_path = "D:\Projects\djhack\static\saves2\zinished{}.jpg".format(
        str(lol))
    cv2.imwrite(new_path, fin)

    lol = lol+1
    time.sleep(1)
    return render_template("something.html", image_name="static\saves2\zinished" + str(lol-1) + ".jpg")


def intensity(level):
    if level == 'low':
        return 30
    if level == 'medium':
        return 20
    if level == 'high':
        return 10


def score_inc(num):
    score = score + num
    return score


@app.route('/webhook', methods=['POST'])
def webhook():
    flag = 0
    data = request.get_json(silent=True)
    score = 0
    if data['queryResult']['intent']['displayName'] == 'feel_happy':
        reply = {
            'fulfillmentText': 'happy works!',
        }
        return jsonify(reply)

    if data['queryResult']['intent']['displayName'] == 'show_song':
        rec_song = song()
        my_string = "{} by {}"
        my_string = my_string.format(
            rec_song['song'][0], rec_song['artist'][0])
        reply = {
            'fulfillmentText': "According to your mood: " + my_string,
        }
        return jsonify(reply)

    if data['queryResult']['intent']['displayName'] == 'doctor_rec':
        city = data['queryResult']['parameters']['geo-city']
        doctors = find(city)
        fin = ""
        for i in range(2):
            my_string = "Doctor {}: \nName: {} Role: {} Contact: {}\n"
            my_string = my_string.format(
                i+1, doctors[i]['Name'], doctors[i]['Role'], doctors[i]['Contact'], )
            fin += my_string

        reply = {
            'fulfillmentText': "Following are the doctor recommendations:\n" + fin
        }
        return jsonify(reply)

    if data['queryResult']['intent']['displayName'] == 'Email':
        sendmail()
        reply = {
            "fulfillmentText": "Email is on its way!"
        }

    # if data['queryResult']['intent']['displayName'] in ['feel_sad - yes - custom', 'feel_sad - yes - custom - custom', 'feel_sad - yes - custom - custom - custom']:
    #     level = data['queryResult']['parameters']
    #     score_inc(intensity(level))

    #     if data['queryResult']['intent']['displayName'] == 'feel_sad - yes - custom - custom - custom':
    #         stg = "Your concern level is {} out of 90."
    #         stg = stg.format(score)
    #         if score >= 30 and score < 50:
    #             reply = {
    #                 'fulfillmentText': stg + "You will be fine! Try playing our mini-games!"
    #             }

    #         elif score >= 50 and score < 70:
    #             reply = {
    #                 'fulfillmentText': stg + "Ask for song recommendations here. Take care, you'll get over it!"
    #             }

    #         elif score >= 70 and score <= 90:
    #             reply = {
    #                 'fulfillmentText': stg + "Please consider getting professional help. We can provide you with recommendations!"
    #             }


def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)
        return response.query_result.fulfillment_text


@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    response_text = {"message":  fulfillment_text}
    return jsonify(response_text)


@app.route('/snake')
def snake():
    print("calls snake!")
    return render_template('snake.html')


@app.route('/')
def home():
    # landing page
    return render_template('home.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/doctor')
def doctor():
    return render_template('doctor.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


# run Flask app
if __name__ == "__main__":
    app.run()
