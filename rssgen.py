import datetime
import sys
import re

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.escape

import PyRSS2Gen

Base = 'http://www.mspaintadventures.com'
AddressRegex = re.compile(r'(\d\d)/(\d\d)/(\d\d).+<a href="(\?s=4[^"]+)">([^<]+)')
def mspa(fn):
    with file(fn, 'r') as f:
        i = 0
        for line in reversed(list(f)):
            m = AddressRegex.match(line)
            if m:
                mm, dd, yy, path, title = m.groups()
                
                yield PyRSS2Gen.RSSItem(
                    title=title,
                    link=Base+path,
                    guid=PyRSS2Gen.Guid(Base+path),
                    description="<html><body>hello</body></html>",
                    pubDate=datetime.datetime(2000+int(yy),int(mm),int(dd), 0, i/60, i%60)
                )
                i += 1

rss = PyRSS2Gen.RSS2(
    title = "Problem Sleuth",
    link = "http://www.mspaintadventures.com",
    description = "Problem Sleuth",

    lastBuildDate = datetime.datetime.utcnow(),

    items = list(
       mspa('mspa.html')
    ))
    
class RSSHandler(tornado.web.RequestHandler):
    def get(self, *args):
        self.set_header('Content-Type', 'application/rss+xml')
        rss.write_xml(self)

handlers = [
    (r"/rss.xml", RSSHandler),
]

application = tornado.web.Application(handlers, default_host='127.0.0.1')

http_server = tornado.httpserver.HTTPServer(application)
http_server.listen(8889)
tornado.ioloop.IOLoop.instance().start()