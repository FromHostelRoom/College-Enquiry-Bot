from chatterbot import ChatBot

from flask import Flask, render_template
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from flask import request
from flask import render_template
from flask import flash
from flask import jsonify
from validate_query import query_validation

app = Flask(__name__)


@app.route("/",methods=['GET'])
def home():
	return render_template("welcome.html")

@app.route("/", methods=['POST'])
def fetch_result():
	message = (request.form['mic-input'])
	x = query_validation(message)
	return x
	

if __name__ == "__main__":
    app.run()