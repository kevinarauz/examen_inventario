from connexion.apps.flask_app import FlaskJSONEncoder
from decimal import Decimal

from datetime import date


def info_encoder(obj):
    if isinstance(obj, date):
        return obj.strftime("%d/%m/%Y")
    if isinstance(obj, Decimal):
        return float(obj)
