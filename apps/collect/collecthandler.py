from ..basehandler import BaseRequestHandler


class CollectHandler(BaseRequestHandler):

    def __init__(self, *args, **kwargs):
        super(CollectHandler, self).__init__(*args, **kwargs)

    def get(self):
        return self.write("hello world")