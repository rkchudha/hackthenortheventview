from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from flask_bootstrap import Bootstrap
from datetime import datetime
import json
import ast
import requests

app = Flask(__name__)
Bootstrap(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/")
def home():
    response = requests.get("https://api.hackthenorth.com/v3/graphql?query={ events { id name event_type permission start_time end_time description speakers { name profile_pic } public_url private_url related_events } }")
    results = response.json()["data"]["events"]
    for event in results:
        start = datetime.fromtimestamp(event['start_time']/ 1000.0)
        end = datetime.fromtimestamp(event['end_time'] / 1000.0)
        event["start_time"] = start.strftime("%I:%M %p")
        event["end_time"] = end.strftime("%I:%M %p")
        event["month_date"] = str(start.strftime("%b")) + str(" ") + str(start.day)
        event["weekday"] = start.strftime("%a")
        for item in event["speakers"]:
            temp = item
        event["host"] = temp["name"]
    return render_template("eventview.html", result=results)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_request", methods=["POST"])
def login_request():
    username = request.form.get("username")
    password = request.form.get("password")
    if username == "hacker" and password == "dog":
        return redirect(url_for('home'))
    else:
        return render_template("error.html", message="incorrect login info")

@app.route("/search/<string:id>")
def search_result(id):
    response = requests.get(
        "https://api.hackthenorth.com/v3/graphql?query={ events { id name event_type permission start_time end_time description speakers { name profile_pic } public_url private_url related_events } }")
    results = response.json()["data"]["events"]
    print("the id requested is " + id)
    print("id type" + str(type(id)))
    for event in results:
        print(event["id"])
        print(str(type(event["id"])))
        if event["id"] == int(id):
            print("found")
            eventresult=""
            eventresult = event
            start = datetime.fromtimestamp(event['start_time'] / 1000.0)
            end = datetime.fromtimestamp(event['end_time'] / 1000.0)
            event["start_time"] = start.strftime("%I:%M %p")
            event["end_time"] = end.strftime("%I:%M %p")
            event["month_date"] = str(start.strftime("%b")) + str(" ") + str(start.day)
            event["weekday"] = start.strftime("%a")
            for item in event["speakers"]:
                temp = item
            event["host"] = temp["name"]
            return render_template("eventdetails.html", event=eventresult)
    return render_template("error.html", message="oops, couldnt access event details")


@app.route("/search/query", methods=["POST"])
def search_request():
    print("Hello world")



if __name__ == "__main__":
    app.run(debug=True)
