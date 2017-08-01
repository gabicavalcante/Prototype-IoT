#!/usr/bin/python

import logging
import logging.config

from logsettings import LOG_SETTINGS

logging.config.dictConfig(LOG_SETTINGS)

from pymongo import MongoClient
from dbsettings import MONGO

client = MongoClient(
    'mongodb://{}:{}@{}/{}'.format(MONGO['username'], MONGO['password'], MONGO['host'], MONGO['database']))

db = client.prototype_database
cards_collection = db.cards


def save_card(card_id):
    logging.debug("Saving card | ID: %s " % card_id)
    h = {'card_id': card_id}
    id = cards_collection.insert_one(h).inserted_id
    print(id)


def remove_card(card_id):
    logging.debug("Removing card | ID: %s " % card_id)
    cards_collection.remove({'card_id': card_id})
    pass


def validate_card(card_id):
    logging.debug("Validating card | ID: %s " % card_id)
    if cards_collection.find({"card_id": card_id}).count() == 0:
        logging.info("VALID CARD")
        return True
    logging.info("INVALID CARD")
    return False


def list_cards():
    return "{card_id: 12345}"
