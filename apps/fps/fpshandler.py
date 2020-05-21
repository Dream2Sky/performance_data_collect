from datetime import datetime
from bson.objectid import ObjectId
from ..basehandler import FPSBaseRequestHandler


class FPSCreateHandler(FPSBaseRequestHandler):

    def __init__(self, *args, **kwargs):
        super(FPSCreateHandler, self).__init__(*args, **kwargs)
        self.t_fps = self.db["t_fps"]

    async def post(self, *args, **kwargs):
        params = self.get_request_json()
        self.t_fps.insert_one(params)


"""
    {
        "filter_dict": {
            "create_time": {
                "gt": "",
                "lt": ""
            },
            "url":""
        },
        "page_size": 20,
        "page_index": 1
    }
"""


class FPSGetHandler(FPSBaseRequestHandler):

    def __init__(self, *args, **kwargs):
        super(FPSGetHandler, self).__init__(*args, **kwargs)
        self.t_fps = self.db["t_fps"]

    async def post(self, *args, **kwargs):

        params = self.get_request_json()
        filter_dict = params.get("filter_dict", {})
        for _k, _v in filter_dict.items():
            if isinstance(_v, dict):
                for _op, _value in _v.items():
                    _op = "${}".format(_op)
        page_index = params.get("page_index", 1)
        page_index = 1 if page_index < 1 else page_index
        page_size = params.get("page_size", 20)
        skip = page_size * (page_index - 1)
        result = self.t_fps.find(filter_dict).limit(page_size).skip(skip)
        data = []
        for item in result:
            item.update({
                "_id": str(item.get("_id"))
            })
            data.append(item)

        self.write({"data": data})
