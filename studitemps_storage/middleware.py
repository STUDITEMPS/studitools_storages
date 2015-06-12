# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext

from .path import FileSystemNotAvailable


class CatchFileSystemNotAvailableMiddleware(object):
    def process_exception(self, request, exception):
        if isinstance(exception, FileSystemNotAvailable):
            response = render_to_response(
                '504.html',
                {'request': request, 'exception': exception},
                RequestContext(request)
            )
            response.status_code = 504
            return response
