# coding: utf-8
#!/usr/bin/env python

import logging.config
import os

import tornado.httpserver  # 引入tornado的一些模块文件
import tornado.ioloop
import tornado.options
from tornado import web
from tornado.options import define, options

logging.config.fileConfig(os.path.join(os.path.dirname(__file__), "../conf/log.conf"), disable_existing_loggers=False)
logger = logging.getLogger(__name__)

define('port', default=9999, help='run on the given port', type=int)

class Application(web.Application):
    def __init__(self):
        from alnews.urls import sub_handlers

        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            #cookie_secret=options.cookie_secret,
            #login_url=options.login_url,
            #static_url_prefix=options.static_url_prefix,

            # auth secret
        )
        web.Application.__init__(self, sub_handlers, **settings)


# Name: MainProcess
# Writer: Heng
# Function: Main process.
def main():
    tornado.options.parse_command_line()

    http_server = tornado.httpserver.HTTPServer(Application(), xheaders=True)
    http_server.listen(options.port)    # Listening port.
    tornado.ioloop.IOLoop.instance().start()  # Start server.


if __name__ == '__main__':  # 文件的入口
    logger.info('==============================logging start==============================')
    main()