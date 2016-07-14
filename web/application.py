#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: zig(shawhen2012@hotmail.com)

import re
import types


class Application(object):
    def __init__(self, patterns):
        self.patterns = patterns
        self.handlers_cls = []
        for tpl in self.patterns:
            url = tpl[0]
            handler_cls = tpl[1]
            kwargs = {}
            if len(tpl) == 3:
                kwargs = tpl[2]
            self.handlers_cls.append((re.compile(url), handler_cls, kwargs))

    def __call__(self, request):
        """

        :param request: web.request.Request
        :return:
        """
        connection = request.connection
        for url_re, handler_cls, kwargs in self.handlers_cls:
            match = url_re.match(request.path)
            if match is not None:
                handler = handler_cls(self, request, **kwargs)
                body = handler()
                if isinstance(body, bytes):
                    body = [body]
                elif isinstance(body, str):
                    body = [body.encode(encoding="latin-1")]
                elif isinstance(body, types.GeneratorType):
                    pass

                response_headers = handler.response_headers
                if connection.headers_sent is False:  # send default headers
                    if isinstance(body, bytes):
                        connection.write_headers(200, "OK", response_headers, chunk=body)
                    else:
                        connection.write_headers(200, "OK", response_headers)
                return body
        else:
            connection.write_headers(404, "Not-Found", {})

            return b""
