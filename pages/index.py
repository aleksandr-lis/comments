import tornado.gen

import config
from core.pages import Base


class Index(Base):

    def post(self):
        pprint(self.request.body)


    @tornado.gen.coroutine
    def get(self):
        cur = yield self.pg.execute(
            'select * from article where id = 1'
        )
        article = cur.fetchone()

        cur = yield self.pg.execute(
            'select * from person where id = 1'
        )
        person = cur.fetchone()

        self.render(
            'index.html',
            article=article,
            person=person,
        )
