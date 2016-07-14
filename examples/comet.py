#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: zig(shawhen2012@hotmail.com)

import zagt
from zagt import web
import gevent
from gevent import pywsgi


class IndexHandler(web.RequestHandler):
    def get(self):
        self.flush_response_headers()

        for i in range(0, 10):
            gevent.sleep(1)
            yield ("the {0}th turn\r\n".format(i)).encode(encoding="latin-1")


if __name__ == "__main__":
    application = web.Application([
        (r"^/$", IndexHandler),
    ])
    wsgi_adapter = web.WSGIAdapter(application)

    wsgi_server = pywsgi.WSGIServer(("localhost", 8000), application=wsgi_adapter)
    wsgi_server.serve_forever()
