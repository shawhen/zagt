#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: zig(shawhen2012@hotmail.com)

from ..http import HTTPConnection


class WSGIConnection(HTTPConnection):
    def __init__(self, method, start_response, remote_addr, protocol):
        super(WSGIConnection, self).__init__(method)

        self.method = method
        self.start_response = start_response
        self.remote_addr = remote_addr
        self.protocol = protocol

        self.headers_sent = False

    def write_headers(self, code, reason, headers, chunk=None, callback=None):
        status, response_headers = super(WSGIConnection, self).make_headers(code, reason, headers, chunk=chunk, callback=callback)

        self.start_response(status, response_headers)
        self.headers_sent = True
        if callback is not None:
            callback()
