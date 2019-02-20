# TODO: Move this to ext
from peewee import *
from peewee import ModelSelect
from playhouse.shortcuts import model_to_dict, dict_to_model



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

    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat()


    if(isinstance(obj, Model)):
        return model_to_dict(obj)


    if(isinstance(obj, ModelSelect)):
        array_out = []
        for item in obj:
            array_out.append(model_to_dict(item))

        return array_out


    return str(obj)


    # raise TypeError ("Type %s not serializable" % type(obj))

def tojson(data):
    return json.dumps(data, default=json_serial)
