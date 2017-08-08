#coding: utf-8
import json

from flask import Flask, Blueprint, render_template, jsonify, request
from flask_restful import Api, Resource, url_for, reqparse, abort

import requests

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import logging
import logging.config
from logsettings import LOG_SETTINGS

logging.config.dictConfig(LOG_SETTINGS)

from logic_control import save_card, list_cards, remove_card, update_card, delete_all_cards, return_card

#
# Setup the API
#
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

parser = reqparse.RequestParser()
parser.add_argument('card_id')


# Card
# shows a single card item and lets you delete a card item
class Card(Resource):
    # TODO: implementar o get
    def get(self, card_id):
        logging.debug("[TODO] GET /card/%s " % card_id)
        card = return_card(card_id)
        return jsonify(card)

    def delete(self, card_id):
        remove_card(card_id)
        logging.debug("DELETE /card/%s " % card_id)
        return '', 204

    # TODO: implementar o put
    def put(self, card_id):
        logging.debug("[TODO] PUT /card/%s " % card_id)
        return '', 201


# Cards
# shows a list of all cards, and lets you POST to add new card
class Cards(Resource):
    def post(self):
        args = parser.parse_args()
        card_id = args['card_id']
        logging.debug("POST /cards %s " % card_id)
        save_card(card_id)
        return '', 201

    def get(self):
        logging.debug("GET /cards ")
        cards = list_cards()
        return jsonify(cards)

    def delete(self):
        logging.debug("DELETE /cards ")
        delete_all_cards()
        return '', 201


api.add_resource(Card, '/cards/<card_id>')
api.add_resource(Cards, '/cards')

#
# Setup the App
#
app = Flask(__name__)
app.register_blueprint(api_bp)

URL = '192.168.99.100'


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/list", methods=['GET'])
def list():
    r = requests.get('http://%s:5000/cards' % URL)
    #if r.text:
    #titles = [x.encode('UTF8') for x in r.text]
    return render_template('index.html', cards=r.text)
    #else:
    #    return render_template('index.html', warning="Sem cartões cadastrados")


@app.route("/clear", methods=['POST'])
def clear():
    r = requests.delete('http://%s:5000/cards' % URL)
    return render_template('index.html', msg="Todos cartões removidos!")


@app.route("/save", methods=['POST'])
def save():
    if not request.form['card_id']:
        error = 'Campo CARD ID vazio!'
        return render_template('index.html', error=error)
    payload = {'card_id': request.form['card_id']}
    r = requests.post('http://%s:5000/cards' % URL, data=payload)
    return render_template('index.html', msg="Cartão salvo!")


@app.route("/remove", methods=['POST'])
def remove():
    if not request.form['card_id']:
        error = 'Campo CARD ID vazio!'
        return render_template('index.html', error=error)
    url = 'http://{}:5000/cards/{}'.format(URL, request.form['card_id'])
    r = requests.delete(url)
    return render_template('index.html', msg="Cartão removido!")


@app.route("/validate", methods=['GET'])
def validate():
    if not request.args.get("card_id"):
        error = 'Campo CARD ID vazio!'
        return render_template('index.html', error=error)
    url = 'http://{}:5000/cards/{}'.format(URL, request.args.get("card_id"))
    r = requests.get(url)

    if bool(r.text):
        msg = "Cartão válido!"
    else:
        msg = "Cartão inválido!"
    return render_template('index.html', msg=msg)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', threaded=True)
