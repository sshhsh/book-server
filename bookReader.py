import json
import linecache
from wsgiref.simple_server import make_server

from elasticsearch import Elasticsearch
from webob import Response, dec


def count_line(file_name):
    count = 0
    file = open(file_name)
    while True:
        buffer = file.read(1024 * 8192)
        if not buffer:
            break
        count += buffer.count('\n')
    file.close()
    return count


@dec.wsgify
def app(request) -> Response:
    print(request.method)
    print(request.path)
    print(request.query_string)
    print(request.GET)
    print(request.POST)
    print(request.params)

    res = Response()

    try:
        if request.path == '/':
            res.status_code = 200
            bid = request.params['id']
            res.headers.add('Access-Control-Allow-Origin', '*')
            res.content_type = 'application/json'
            res.charset = 'utf-8'
            n = count_line(bid)
            doc = {
                "len": n / 100
            }
            res.body = json.dumps(doc).encode()
        elif request.path == '/read':
            bid = request.params['id']
            chapter_id = int(request.params['chapter'])
            res.headers.add('Access-Control-Allow-Origin', '*')
            res.content_type = 'application/json'
            res.charset = 'utf-8'
            chapters = []
            for i in range(chapter_id * 100 + 1, chapter_id * 100 + 101):
                c = linecache.getline(bid, i)
                if not c:
                    break
                elif c[-1] == '\n':
                    c = c[:-1]
                chapters.append(c)
            title = es.get(index='ebooks', doc_type='book', id=bid)['_source']['title']

            doc = {
                "t": title,
                "p": chapters
            }
            res.body = json.dumps(doc).encode()
        else:
            res.status_code = 404
            res.body = '<h1>Not found</h1>'.encode()
    except Exception as e:
        print(e)
        res.status_code = 404
        res.body = '<h1>Not found</h1>'.encode()
    return res


if __name__ == '__main__':
    es = Elasticsearch(hosts="172.17.0.1:19200")
    ip = '0.0.0.0'
    port = 9999
    server = make_server(ip, port, app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        server.server_close()
