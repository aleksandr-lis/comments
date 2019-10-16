import tornado.gen

import config
from core.pages import Base


class Index(Base):

    def post(self):
        pprint(self.request.body)


    @tornado.gen.coroutine
    def get(self):
        article_fut = self.pg.execute(
            'select * from article where id = 1'
        )
        person_fut = self.pg.execute(
            'select * from person where id = 1'
        )

        yield [article_fut, person_fut]
        article = article_fut.result().fetchone()
        person = person_fut.result().fetchone()

        self.render(
            'index.html',
            article=article,
            person=person,
        )
