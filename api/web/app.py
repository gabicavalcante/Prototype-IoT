import logging
import logging.config

from flask import Flask, Blueprint, render_template, request
from flask_restful import Api, Resource, reqparse, abort

from logsettings import LOG_SETTINGS

logging.config.dictConfig(LOG_SETTINGS)

# from logic_control import list_cards, save_card, remove_card

#
# Setup the API
#
app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('card_id')

CARDS = {}


def abort_if_card_id_doesnt_exist(card_id):
    if card_id not in CARDS:
        logging.error("Card {} doesn't exist".format(card_id))
        abort(404, message="Card {} doesn't exist".format(card_id))


# Card
# shows a single card item and lets you delete a card item
class Card(Resource):
    def get(self, card_id):
        abort_if_card_id_doesnt_exist(card_id)

        logging.debug("GET /card/%s " % card_id)
        return CARDS[card_id]

    def delete(self, card_id):
        abort_if_card_id_doesnt_exist(card_id)
        del CARDS[card_id]

        logging.debug("DELETE /card/%s " % card_id)
        return '', 204

    def put(self, card_id):
        abort_if_card_id_doesnt_exist(card_id)
        card = {card_id: ''}
        CARDS[card_id] = card

        logging.debug("PUT /card/%s " % card_id)
        return card, 201


# Cards
# shows a list of all cards, and lets you POST to add new card
class Cards(Resource):
    def post(self):
        args = parser.parse_args()
        card_id = args['card_id']
        CARDS.update({card_id: ''})
        logging.debug("POST /cards %s " % card_id)
        return card_id, 201

    def get(self):
        logging.debug("GET /cards ")
        return CARDS, 201


api.add_resource(Card, '/card/<card_id>')
api.add_resource(Cards, '/cards')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
