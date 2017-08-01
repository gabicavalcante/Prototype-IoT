from flask import Flask, Blueprint, render_template, jsonify, request
from flask_restful import Api, Resource, url_for, reqparse

import requests

# from logic_control import list_cards, save_card, remove_card

#
# Setup the API
#
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

parser = reqparse.RequestParser()
parser.add_argument('card_id')


class Card(Resource):
    def delete(self, card_id):
        return '', 201
        # return remove_card(card_id), 201


class Cards(Resource):
    def post(self):
        args = parser.parse_args()
        card_id = args['card_id']
        print('ok')
        # save_card(card_id)
        return card_id, 201

    def get(self):
        return '{OK}', 201
        # return list_cards(), 201


api.add_resource(Card, '/card/<card_id>')
api.add_resource(Cards, '/cards')

#
# Setup the App
#
app = Flask(__name__)
app.register_blueprint(api_bp)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/list", methods=['GET'])
def list():
    return requests.get('http://192.168.99.100:5000/cards').content


@app.route("/save", methods=['POST'])
def save():
    data = {'card_id': request.form['card_id']}
    r = requests.post('http://127.0.0.1:5000/cards', data)
    return r.status_code, data['card_id']


@app.route("/remove", methods=['GET'])
def remove():
    return requests.get('http://127.0.0.1:5000/cards').content


@app.route("/validate", methods=['GET'])
def validate():
    return requests.get('http://127.0.0.1:5000/cards').content


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
