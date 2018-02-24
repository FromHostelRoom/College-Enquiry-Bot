from flask import Flask
from flask import render_template
from flask import flash
from flask import jsonify
from flask import request
from validate_query import query_validation

app = Flask(__name__)

@app.route("/",methods=['GET'])
def home():
	return render_template("welcome.html")

@app.route("/", methods=['POST'])
def fetch_result():
	if(request.form['mic-input']):
		message = request.form['mic-input']
	if(request.form['type-input']):
		message = request.form['type-input']
	x = query_validation(message)
	return x
	

if __name__ == "__main__":
    app.run()