from flask import Flask, Blueprint, render_template, request

import requests

#
# Setup the App
#
app = Flask(__name__)

URL = '192.168.99.100'


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/list", methods=['GET'])
def list():
    return requests.get('http://%s:5000/cards' % URL).content


@app.route("/save", methods=['POST'])
def save():
    data = {'card_id': request.form['card_id']}
    r = requests.post('http://%s:5000/cards' % URL, data)
    return r.status_code


@app.route("/remove", methods=['GET'])
def remove():
    return requests.get('http://%s:5000/cards' % URL).content


@app.route("/validate", methods=['GET'])
def validate():
    return requests.get('http://%s:5000/cards' % URL).content


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
