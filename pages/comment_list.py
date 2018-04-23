from pprint import pprint
import datetime
import tornado.gen

import config
from core.pages import Base


class CommentList(Base):

    @tornado.gen.coroutine
    def post(self):

        # Incoming

        article_id = self.get_body_argument('article_id', default=None)
        comment_id = self.get_body_argument('comment_id', default=None)
        person_id = self.get_body_argument('person_id', default=None)

        fill_threads = self.get_body_argument('threads', default='no').lower() == 'yes'

        try:
            page = int(self.get_body_argument('page', default=1))
            if page <= 0:
                page = 1
        except ValueError:
            page = 1

        # Query

        comments = []
        rows = []
        childs = []

        if article_id:
            cur = yield self.pg.execute(
                'select c.*, p.name as person from comment as c, person as p '
                'where c.person_id = p.id and c.article_id = %s and c.thread_id is null '
                'and c.is_deleted is false '
                'order by c.created asc offset %s limit %s ', (
                    article_id,
                    (page - 1) * config.COMMENTS_ON_PAGE,
                    config.COMMENTS_ON_PAGE,
                )
            )
            rows = cur.fetchall()

        if comment_id:
            cur = yield self.pg.execute(
                'select c.*, p.name as person from comment as c, person as p '
                'where c.person_id = p.id and c.id = %s '
                'and c.is_deleted is false '
                'order by c.created asc offset %s limit %s ', (
                    comment_id,
                    (page - 1) * config.COMMENTS_ON_PAGE,
                    config.COMMENTS_ON_PAGE,
                )
            )
            rows = cur.fetchall()

        if person_id:
            cur = yield self.pg.execute(
                'select * from comment '
                'where person_id = %s '
                'and is_deleted is false '
                'order by created asc offset %s limit %s ', (
                    person_id,
                    (page - 1) * config.COMMENTS_ON_PAGE,
                    config.COMMENTS_ON_PAGE,
                )
            )
            rows = cur.fetchall()


        # Threads

        if fill_threads:
            parents = []
            for row in rows:
                parents.append(row.id)

            cur = yield self.pg.execute(
                'select c.*, p.name as person from comment as c, person as p '
                'where c.person_id = p.id and c.thread_id = any(%s) '
                'and c.is_deleted is false '
                'order by c.created asc ', (
                    parents,
                )
            )
            childs = cur.fetchall()


        # Result

        for row in rows:
            comments.append(
                self._prepare(row, childs)
            )

        self.json(comments)


    def _prepare(self, item, childs):
        res = {
            'id': item.id,
            'created': datetime.datetime.strftime(
                item.created, '%d.%m.%Y %H:%I'
            ),
            'content': item.content,
        }

        if hasattr(item, 'person'):
            res['person'] = item.person

        # Childs

        res['childs'] = []

        for child in childs:
            if child.parent_id == item.id:
                res['childs'].append(
                    self._prepare(child, childs)
                )

        # Result

        return res
