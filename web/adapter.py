#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: zig(shawhen2012@hotmail.com)

import wsgiref
from wsgiref import util

from ..wsgi import WSGIConnection

from . import request as m_request


class WSGIAdapter(object):
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        REQUEST_METHOD = environ["REQUEST_METHOD"]
        PATH_INFO = environ["PATH_INFO"]
        remote_ip = environ.get("REMOTE_ADDR", "")
        protocol = wsgiref.util.guess_scheme(environ)
        uri = wsgiref.util.request_uri(environ)
        headers = {}
        if environ.get("CONTENT_TYPE"):
            headers["Content-Type"] = environ["CONTENT_TYPE"]
        if environ.get("CONTENT_LENGTH"):
            headers["Content-Length"] = environ["CONTENT_LENGTH"]
        for key in environ:
            if key.startswith("HTTP_"):
                headers[key[5:].replace("_", "-")] = environ[key]
        body = None
        if headers.get("Content-Length"):
            body = environ["wsgi.input"].read(
                int(headers["Content-Length"]))

        connection = WSGIConnection(REQUEST_METHOD, start_response, remote_ip, protocol)
        request = m_request.Request(REQUEST_METHOD, uri, PATH_INFO, "HTTP/1.1", headers, body=body, connection=connection)

        body = self.application(request)

        return body
