from pprint import pprint
import datetime
import tornado.gen

import config
from core.pages import Base


class CommentLog(Base):

    @tornado.gen.coroutine
    def post(self):

        # Incoming

        comment_id = self.get_body_argument('comment_id', default=None)

        # Query

        logs = []
        rows = []

        cur = yield self.pg.execute(
            'select l.*, p.name as person from log as l, person as p '
            'where l.person_id = p.id and comment_id = %s '
            'order by created ', (
                comment_id,
            )
        )
        rows = cur.fetchall()

        # Result

        for row in rows:
            logs.append(
                self._prepare(row)
            )

        self.json(logs)


    def _prepare(self, item):
        res = {
            'id': item.id,
            'created': datetime.datetime.strftime(
                item.created, '%d.%m.%Y %H:%I'
            ),
            'type': item.type,
            'person': item.person,
            'before': item.before,
            'after': item.after,
        }
        return res
