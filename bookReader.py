import json
from wsgiref.simple_server import make_server
from webob import Request, Response, dec


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
        res.headers.add('Access-Control-Allow-Origin', '*')
        res.content_type = 'application/json'
        res.charset = 'utf-8'
        doc = {
            "len": 10
        }
        res.body = json.dumps(doc).encode()
    elif request.path == '/read':
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