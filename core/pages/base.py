import json
import tornado.web
from dicttoxml import dicttoxml

import config


class Base(tornado.web.RequestHandler):

    @property
    def app(self):
        return self.application

    @property
    def pg(self):
        return self.application.pg

    def render(self, template, *args, **kwargs):
        try:
            post = dict()
            get = dict()
            for arg in self.request.arguments:
                if self.get_body_argument(arg, default=None):
                    post[arg] = self.get_body_argument(arg)
                if self.get_query_argument(arg, default=None):
                    get[arg] = self.get_query_argument(arg)

            super().render(template, config=config, post=post, get=get, *args, **kwargs)
        except RuntimeError:
            pass


    def json(self, answer, *args, **kwargs):
        self.set_header('Content-Type', 'application/json')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Cache-Control', 'no-cache')
        self.write(json.dumps(answer))
        self.finish()


    def xml(self, answer, root, *args, **kwargs):
        xml = dicttoxml(answer, custom_root=root, attr_type=False)
        
        self.set_header('Content-Type', 'application/force-download')
        self.set_header('Content-Disposition', 'attachment; filename=download.xml')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Cache-Control", "no-cache")
        self.write(xml)
        self.finish()
