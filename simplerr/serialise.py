# TODO: Move this to ext
from peewee import ModelSelect, Model
from playhouse.shortcuts import model_to_dict

# We need custom json_serial to handle date time - not supported
# by the default json_dumps
#
# See https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable

import json
from datetime import date, datetime, time


# TODO: All serialisable items need to have a obj.todict() method, otheriwse
# str(obj) will be used.
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime):
        return obj.isoformat(' ')

    if isinstance(obj, (date, time)):
        return obj.isoformat()

    if isinstance(obj, Model):
        return model_to_dict(obj)

    if isinstance(obj, ModelSelect):
        return [ model_to_dict(item) for item in obj ]

    return str(obj)


def tojson(data):
    return json.dumps(data, default=json_serial)
