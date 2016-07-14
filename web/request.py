#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: zig(shawhen2012@hotmail.com)

import abc
import urllib
from urllib import parse


class Request(object):
    def __init__(self, method, uri, path, version, headers, body=None, connection=None):
        self.method = method
        self.uri = uri
        self.version = version
        self.headers = headers
        self.body = body or b""
        self.connection = connection
        self.path = path

        _, _, self.query  = self.uri.partition("?")
        self.query_arguments = parse.parse_qs(self.query, encoding="latin-1", errors="strict")
        self.body_arguments = {}


class RequestHandler(object):
    def __init__(self, application, request, **kwargs):
        self.application = application
        self.request = request
        self.kwargs = kwargs

        self.response_headers = {}

    def __call__(self):
        if self.request.method == "HEAD":
            return self.head()
        elif self.request.method == "GET":
            return self.get()
        elif self.request.method == "POST":
            return self.post()

    def add_response_header(self, key, value):
        self.response_headers[key] = str(value)

    def flush_response_headers(self, chunk_encoding=True, content_type="text/html"):
        if chunk_encoding:
            if "Content-Type" not in self.response_headers:
                self.response_headers["Content-Type"] = content_type
        self.request.connection.write_headers(200, "OK", self.response_headers)

    def get_argument(self, key, default=[], strip=True):
        value = self.get_query_argument(key, default, strip)
        if value is default:  # can't find in query arguments
            value = self.get_body_argument(key, default, strip)
        else:  # provide default or find in query arguemtns
            return value
        if value is default:  # can't find in query&body arguments
            raise ValueError("Missing argument: {0}".format(key))
        else:  # provide default or find in body arguments
            return value

    def get_query_argument(self, key, default=[], strip=True):
        if key in self.request.query_arguments:
            return self.request.query_arguments[key][0]
        else:
            return default

    def get_body_argument(self, key, default=[], strip=True):
        if key in self.request.body_arguments:
            return self.request.body_arguments[key][0]
        else:
            return default

    @abc.abstractclassmethod
    def head(self):
        raise NotImplementedError()

    @abc.abstractclassmethod
    def get(self):
        raise NotImplementedError()

    @abc.abstractclassmethod
    def post(self):
        raise NotImplementedError()
