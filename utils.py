import threading
import json
import datetime
from decimal import Decimal


mu = threading.Lock()

def singleton(cls):
    instances = {}

    def _singleton(*args, **kwargs):
        def create_new(*new_args, **new_kwargs):
            if mu.acquire():
                if cls not in instances:
                    instances[cls] = cls(*new_args, **new_kwargs)
                mu.release()
                return instances[cls]

        if cls not in instances:
            return create_new(*args, **kwargs)
        return instances[cls]

    return _singleton


class DateEncoder(json.JSONEncoder):

    def default(self, o):    # pylint: disable=E0202
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        elif isinstance(o, Decimal):
            return float(o)
        else:
            return json.JSONEncoder.default(self, o)