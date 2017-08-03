#!/usr/bin/python
import os
import logging
import logging.config

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

from logsettings import LOG_SETTINGS

logging.config.dictConfig(LOG_SETTINGS)

# Connection to Mongo DB
try:
    client = MongoClient(os.environ['DB_PORT_27017_TCP_ADDR'], 27017)
    db = client.prototypedb
    cards_collection = db.cards
    logging.debug("Connected MongoDB successfully")
except ConnectionFailure as e:
    logging.debug("Could not connect to MongoDB: %s" % e)


def save_card(card_id):
    try:
        logging.debug("Saving card | ID: %s " % card_id)
        item = {'card_id': card_id}
        cards_collection.insert_one(item)
    except OperationFailure as e:
        logging.debug("Could not insert ID Card to MongoDB: %s" % e)


# TODO: implementar update
def update_card(card_id):
    try:
        card = cards_collection.find_one({'card_id': card_id})

        if card is not None:
            card['card_id'] = card_id
            cards_collection.save(card)

    except OperationFailure as e:
        logging.debug("Could not update ID Card to MongoDB: %s" % e)


def remove_card(card_id):
    try:
        logging.debug("Removing card | ID: %s " % card_id)
        cards_collection.remove({'card_id': card_id})
    except OperationFailure as e:
        logging.debug("Could not remove ID Card to MongoDB: %s" % e)


def validate_card(card_id):
    logging.debug("Validating card | ID: %s " % card_id)
    if cards_collection.find({"card_id": card_id}).count() == 0:
        logging.info("VALID CARD")
        return True
    logging.info("INVALID CARD")
    return False


def return_card(card_id):
    logging.debug("Return card | ID: %s " % card_id)
    if cards_collection.find({"card_id": card_id}).count() == 0:
        return cards_collection.find({"card_id": card_id})
    logging.info("INVALID CARD")
    return False


def list_cards():
    cards = []
    for card in cards_collection.find():
        card.pop('_id')
        cards.append(card)

    return cards


def delete_all_cards():
    client.drop_database('prototypedb')

