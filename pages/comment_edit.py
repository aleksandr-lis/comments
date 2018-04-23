from pprint import pprint
import datetime
import tornado.gen

import config
from core.pages import Base


class CommentEdit(Base):

    @tornado.gen.coroutine
    def post(self):

        person = None
        person_fut = None

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

        if self.get_body_argument('comment_id', default=None):
            comment_fut = self.pg.execute(
                'select * from comment where id = %s ', (
                    self.get_body_argument('comment_id'),
                )
            )

        yield person_fut
        person = person_fut.result().fetchone()

        if comment_fut:
            yield comment_fut
            comment = comment_fut.result().fetchone()

        # Checks

        if not comment:
            return self.json({
                'error': 'Wrong request',
            })

        if comment.person_id != person.id:
            return self.json({
                'error': 'Access denied',
            })

        # Query

        content_new = self.get_body_argument('content', default='Did\'t say anything')

        comment_fut = self.pg.execute(
            'update comment set content = %s where id = %s returning * ', (
                content_new,
                comment.id,
            )
        )

        # Log

        log_fut = self.pg.execute(
            'insert into log (type, comment_id, person_id, before, after) values (%s, %s, %s, %s, %s) ', (
                'u',
                comment.id,
                person.id,
                comment.content,
                content_new,
            )
        )

        # Result

        yield [comment_fut, log_fut]
        comment_new = comment_fut.result().fetchone()

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
