#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: zig(shawhen2012@hotmail.com)

import abc


class HTTPConnection(object):
    def __init__(self, method):
        self.method = method

    def make_headers(self, code, reason, headers, chunk=None, callback=None):
        """

        :param start_line:
        :param headers: a dict of all header
        :param callback:
        :return:
        """
        if self.method == "HEAD":
            expected_content_len = 0
        elif "Content-Length" in headers:
            expected_content_len = (headers["Content-Length"])
        else:
            expected_content_len = None
        if chunk is not None:
            expected_content_len = len(chunk)
        if expected_content_len is not None:
            headers["Content-Length"] = expected_content_len

        status = "{0} {1}".format(code, reason)
        response_headers = []
        for k, v in headers.items():
            response_headers.append((str(k), str(v)))
        return status, response_headers

    @abc.abstractclassmethod
    def write_headers(self, code, reason, headers, chunk=None, callback=None):
        raise NotImplementedError()
