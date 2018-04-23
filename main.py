#! /usr/bin/env python3

import os
import sys
import psycopg2
import tornado.ioloop
import tornado.web
import momoko

import pages
import config


def start():

    app = tornado.web.Application([
        (r'^/$', pages.Index),
        (r'^/comment/list/$', pages.CommentList),
        (r'^/comment/add/$', pages.CommentAdd),
        (r'^/comment/edit/$', pages.CommentEdit),
        (r'^/comment/delete/$', pages.CommentDelete),
        (r'^/comment/log/$', pages.CommentLog),
        (r'^/comment/download/$', pages.CommentDownload),
    ], **{
        'debug': config.DEBUG,
        'static_path': os.path.join(config.ROOT, 'static'),
        'template_path': os.path.join(config.ROOT, 'templates'),
    })

    ioloop = tornado.ioloop.IOLoop.instance()

    # Postgres

    app.pg = momoko.Pool(
        dsn=config.PG_DSN,
        size=1,
        max_size=config.PG_POOL_SIZE,
        cursor_factory=psycopg2.extras.NamedTupleCursor,
        ioloop=ioloop,
    )

    future = app.pg.connect()
    ioloop.add_future(future, lambda f: ioloop.stop())
    ioloop.start()

    # Server

    app.listen(config.PORT)
    ioloop.start()


def migrate():
    con = psycopg2.connect(config.PG_DSN)
    con.set_session(autocommit=True)
    cur = con.cursor()
    sql = open(os.path.join(config.ROOT, '_init.sql')).read()
    cur.execute(sql)


if __name__ == '__main__':

    if len(sys.argv) > 1:
        if sys.argv[1] == 'migrate':
            migrate()
    else:
        start()
