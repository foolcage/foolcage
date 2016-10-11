from scrapy.http import Response


class GetFileMiddleware(object):
    def process_request(self, request, spider):
        if request.url == 'http://www.fakeurl.com':
            return Response('http://www.fakeurl.com')
