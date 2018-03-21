from flask import Flask
from flask import render_template
from flask import flash
from flask import jsonify
from flask import request
from backend.validate_query import query_validation
from backend.train_func import train_query_classifier, train_general_query_classifier,train_specific_query_classifier
import sys


app = Flask(__name__)

#train_query_classifier()
#train_general_query_classifier()
#train_specific_query_classifier()
#train_ner("backend/training_data/general/ner_general_query_dataset.txt")
#sys.exit()

@app.route("/",methods=['GET'])
def home():

	return render_template("welcome.html")

@app.route("/", methods=['POST'])
def fetch_result():
	if(request.form['mic-input']):
		message = request.form['mic-input']
	if(request.form['type-input']):
		message = request.form['type-input']
	message = message.lower()
	x = query_validation(message)
	return x
	

if __name__ == "__main__":
    app.run()