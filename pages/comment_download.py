from pprint import pprint
import datetime
import tornado.gen

import config
from core.pages import Base


class CommentDownload(Base):

    @tornado.gen.coroutine
    def post(self):

        # Incoming

        try:
            date_from = datetime.datetime.strptime(
                self.get_body_argument('date_from'),
                '%d.%m.%Y',
            ).date()
        except ValueError:
            date_from = datetime.date(1970, 1, 1)

        try:
            date_to = datetime.datetime.strptime(
                self.get_body_argument('date_to'),
                '%d.%m.%Y',
            ).date()
        except ValueError:
            date_to = datetime.datetime.now()

        article_id = self.get_body_argument('article_id', default=None)
        person_id = self.get_body_argument('person_id', default=None)
        file_format = self.get_body_argument('file_format', default='xml')

        # Query

        comments = []
        rows = []

        if article_id:
            cur = yield self.pg.execute(
                'select c.*, p.name as person from comment as c, person as p '
                'where c.person_id = p.id and c.article_id = %s and c.created >= %s and c.created <= %s '
                'and c.is_deleted is false '
                'order by c.created asc ', (
                    article_id,
                    date_from,
                    date_to,
                )
            )
            rows = cur.fetchall()

        if person_id:
            cur = yield self.pg.execute(
                'select c.*, p.name as person from comment as c, person as p '
                'where c.person_id = p.id and c.person_id = %s and c.created >= %s and c.created <= %s '
                'and c.is_deleted is false '
                'order by c.created asc ', (
                    person_id,
                    date_from,
                    date_to,
                )
            )
            rows = cur.fetchall()

        # Result

        for row in rows:
            comments.append(
                self._prepare(row)
            )

        if file_format == 'xml':
            return self.xml(comments, 'comments')
        else:
            return self.json({
                'error': 'Unknown format',
            })

        # self.json(comments)


    def _prepare(self, item):
        res = {
            'id': item.id,
            'parent_id': item.parent_id,
            'thread_id': item.thread_id,
            'article_id': item.article_id,
            'person_id': item.person_id,
            'person': None,
            'created': datetime.datetime.strftime(
                item.created, '%d.%m.%Y %H:%I'
            ),
            'content': item.content,
        }

        if hasattr(item, 'person'):
            res['person'] = item.person

        return res
