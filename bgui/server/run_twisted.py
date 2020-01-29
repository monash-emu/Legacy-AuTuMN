import os
import sys
import shutil

from twisted.internet import reactor
from twisted.internet.endpoints import serverFromString
from twisted.logger import globalLogBeginner, FileLogObserver, formatEvent
from twisted.web.resource import Resource
from twisted.web.server import Site
from twisted.web.static import File
from twisted.web.wsgi import WSGIResource
from twisted.python.threadpool import ThreadPool

from server import config
from server.api import app

import autoreload

def run_app_in_twisted():
    globalLogBeginner.beginLoggingTo([
        FileLogObserver(sys.stdout, lambda _: formatEvent(_) + "\n")])

    threadpool = ThreadPool(maxthreads=30)
    wsgi_app = WSGIResource(reactor, threadpool, app)

    class ServerResource(Resource):
        isLeaf = True

        def __init__(self, wsgi):
            Resource.__init__(self)
            self._wsgi = wsgi

        def render(self, request):
            """
            Adds headers to disable caching of api calls
            """
            request.prepath = []
            request.postpath = ['api'] + request.postpath[:]
            r = self._wsgi.render(request)
            request.responseHeaders.setRawHeaders(
                b'Cache-Control',
                [b'no-cache', b'no-store', b'must-revalidate'])
            request.responseHeaders.setRawHeaders(b'expires', [b'0'])
            return r

    # web-client files served from here
    base_resource = File('../client/dist')

    # api requests must go through /api
    base_resource.putChild('api', ServerResource(wsgi_app))

    # downloadable files go here
    base_resource.putChild('file', File(config.SAVE_FOLDER))

    site = Site(base_resource)

    # Start the threadpool now, shut it down when we're closing
    threadpool.start()
    reactor.addSystemEventTrigger('before', 'shutdown', threadpool.stop)

    endpoint = serverFromString(reactor, "tcp:port=" + str(config.PORT))
    endpoint.listen(site)

    reactor.run()


if __name__ == "__main__":
    autoreload.main(run_app_in_twisted)
