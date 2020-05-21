import json
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from tornado.web import RequestHandler
from tornado.escape import to_unicode, utf8
from tornado.util import unicode_type
from db import fps_mongo_db, collect_mongo_db
from utils import DateEncoder

class BaseRequestHandler(RequestHandler):
    executor = ThreadPoolExecutor(max_workers=200)
    def __init__(self, *args, **kwargs):
        super(BaseRequestHandler, self).__init__(*args, **kwargs)
    
    def write(self, chunk):
        if self._finished:
            raise RuntimeError("Cannot write() after finish()")
        if not isinstance(chunk, (bytes, unicode_type, dict)):
            message = "write() only accepts bytes, unicode, and dict objects"
            if isinstance(chunk, list):
                message += ". Lists not accepted for security reasons; see " + \
                           "http://www.tornadoweb.org/en/stable/web.html#tornado.web.RequestHandler.write"
            raise TypeError(message)
        if isinstance(chunk, dict):
            # 返回数据库数据中存在datetime、date，decimal格式，原write会报错
            chunk = json.dumps(chunk, cls=DateEncoder).replace("</", "<\\/")
            self.set_header("Content-Type", "application/json; charset=UTF-8")
        chunk = utf8(chunk)
        self._write_buffer.append(chunk)

    def get_request_arguments(self):
        return {key: value[0].decode() for key, value in list(self.request.arguments.items())}

    def get_request_json(self):
        try:
            params_json = json.loads(self.request.body.decode("utf-8", "ignore"), strict=False)
            params_json.update({
                "create_time": datetime.now()
            })
            return params_json
        except ValueError:
            logging.error(self.request.body)

class CollectBaseRequestHandler(BaseRequestHandler):
    
    def __init__(self, *args, **kwargs):
        super(CollectBaseRequestHandler, self).__init__(*args, **kwargs)
        self.db = collect_mongo_db

class IndexHandler(BaseRequestHandler):
    
    def get(self, *args, **kwargs):
        self.render("index.html")

class FPSBaseRequestHandler(BaseRequestHandler):
    
    def __init__(self, *args, **kwargs):
        super(FPSBaseRequestHandler, self).__init__(*args, **kwargs)
        self.db = fps_mongo_db