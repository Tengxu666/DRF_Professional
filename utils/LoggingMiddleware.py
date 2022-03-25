from __future__ import unicode_literals
import logging
import time


class LoggingMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # try:
        #     body = json.loads(request.body)
        # except Exception:
        #     body = dict()
        # body.update(dict(request.POST))
        try:
            res = response.data
        except Exception:
            res = None
        if request.method != 'GET':
            localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            logging.info("{} {} {} {} {} {}\nres:{}".format(
                localtime, request.user, request.method, request.path,
                response.status_code, response.reason_phrase, res))
        return response
