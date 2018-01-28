from flask import Flask

app = Flask(__name__)

@app.route("/")
def main():
  return "haha"

@app.route("/start")
def start():
  return "gg"

app.run()
