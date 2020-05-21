import tornado.web
import tornado.httpserver
import tornado.ioloop
import platform
import os

from apps.collect.collecthandler import CollectHandler
from apps.fps.fpshandler import FPSCreateHandler, FPSGetHandler
from apps.basehandler import IndexHandler

# windows 必备
if platform.system() == "Windows":
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Application(tornado.web.Application):

    def __init__(self):
        tornado.web.Application.__init__(self, handlers=[
            (r"/index", IndexHandler),
            (r"/fps_create", FPSCreateHandler),
            (r"/fps_get", FPSGetHandler)
        ], template_path=os.path.join(
            os.path.dirname(__file__), "templates"  # 索引到templates文件夹中的html
        ),static_path=os.path.join(os.path.dirname(__file__), "static"), debug=True)


if __name__ == "__main__":
    app = Application()
    http_server = tornado.httpserver.HTTPServer(app, xheaders=True)

    http_server.listen(8227)
    tornado.ioloop.IOLoop.instance().start()
