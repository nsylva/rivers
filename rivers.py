from flask import Flask, render_template, request
import json
import requests

app = Flask(__name__)


@app.route("/")
def home():
	return render_template("project.html")


if __name__ == '__main__':
	app.run(port=5000,debug = True)

