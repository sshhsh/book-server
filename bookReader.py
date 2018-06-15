import json
import math
from wsgiref.simple_server import make_server
from webob import Request, Response, dec


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

    if request.path == '/':
        res.status_code = 200
        bid = request.params['id']
        res.headers.add('Access-Control-Allow-Origin', '*')
        res.content_type = 'application/json'
        res.charset = 'utf-8'
        n = count_line(bid)
        doc = {
            "len": int(math.ceil(n/100))
        }
        res.body = json.dumps(doc).encode()
    elif request.path == '/read':
        bid = request.params['id']
        chapter_id = request.params['chapter']
        res.headers.add('Access-Control-Allow-Origin', '*')
        res.content_type = 'application/json'
        res.charset = 'utf-8'
        doc = {
            "t": "the first",
            "p": ["aaa", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc", "bbb", "ccc"]
        }
        res.body = json.dumps(doc).encode()
    else:
        res.status_code = 404
        res.body = '<h1>Not found</h1>'.encode()
    return res


if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 9999
    server = make_server(ip, port, app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
        server.server_close()