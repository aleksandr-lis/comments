from pprint import pprint
import datetime
import tornado.gen

import config
from core.pages import Base


class CommentAdd(Base):

    @tornado.gen.coroutine
    def post(self):

        person = None
        person_fut = None

        article = None
        article_fut = None

        comment = None
        comment_fut = None

        # Data

        if self.get_body_argument('sid', default=None) == 'some_session_id':
            person_fut = self.pg.execute(
                'select * from person where sid = %s ', (
                    self.get_body_argument('sid'),
                )
            )
        else:
            return self.json({
                'error': 'Wrong SID',
            })

        if self.get_body_argument('article_id', default=None):
            article_fut = self.pg.execute(
                'select * from article where id = %s ', (
                    self.get_body_argument('article_id'),
                )
            )

        if self.get_body_argument('comment_id', default=None):
            comment_fut = self.pg.execute(
                'select * from comment where id = %s ', (
                    self.get_body_argument('comment_id'),
                )
            )

        yield person_fut
        person = person_fut.result().fetchone()

        if article_fut:
            yield article_fut
            article = article_fut.result().fetchone()

        if comment_fut:
            yield comment_fut
            comment = comment_fut.result().fetchone()

        # Checks

        if not article and not comment:
            return self.json({
                'error': 'Wrong request',
            })

        # Query

        if comment:
            comment_id = comment.id
            if comment.thread_id:
                thread_id = comment.thread_id
            else:
                thread_id = comment.id
            article_id = comment.article_id
        else:
            comment_id = None
            thread_id = None
            article_id = None

        if article:
            article_id = article.id

        content = self.get_body_argument('content', default='Did\'t say anything')

        cur = yield self.pg.execute(
            'insert into comment (parent_id, thread_id, article_id, person_id, content) values (%s, %s, %s, %s, %s) returning * ', (
                comment_id,
                thread_id,
                article_id,
                person.id,
                content,
            )
        )
        comment_new = cur.fetchone()

        # Log

        yield self.pg.execute(
            'insert into log (type, comment_id, person_id, after) values (%s, %s, %s, %s) ', (
                'i',
                comment_new.id,
                person.id,
                content,
            )
        )

        # Result

        self.json([
            self._prepare(comment_new)
        ])


    def _prepare(self, item):
        res = {
            'id': item.id,
            'created': datetime.datetime.strftime(
                item.created, '%d.%m.%Y %H:%I'
            ),
            'content': item.content,
        }
        return res
