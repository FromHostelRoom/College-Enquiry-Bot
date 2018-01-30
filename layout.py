from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def main():
  return render_template("welcome.html")

@app.route("/start")
def start():
  return "gg"

app.run()
