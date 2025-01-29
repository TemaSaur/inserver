from __future__ import annotations
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Callable
import re
import json


class Request:
    def __init__(self, request):
        pass


class Response:
    response_code: int
    headers: dict[str, str]
    body: bytes

    def __init__(self) -> None:
        self.headers = {}
        self.body = bytes()

    def json(
        self,
        response_code: int,
        body: dict | str | bytes,
        headers: dict[str, str] | None = None,
        encoding: str = "utf-8"
    ):
        self.response_code = response_code

        self.headers["Content-Type"] = "application/json"

        if headers is not None:
            self.headers |= headers

        if isinstance(body, dict):
            body = json.dumps(body)

        if isinstance(body, str):
            body = bytes(body, encoding=encoding)

        self.body = body


class Application:
    handlers: dict[str, dict[str, Callable]]
    address: tuple[str, int]

    class Handler(BaseHTTPRequestHandler):
        app: Application

        def do(self, method: str):
            for p, h in self.app.handlers[method].items():
                if re.match(p, self.path):
                    self.serve(h)
                    return

            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(b'"not found"')

        def serve(self, handler):
            request = Request(self.request)
            response = Response()

            handler(request=request, response=response)

            self.send_response(response.response_code)
            for h, v in response.headers.items():
                self.send_header(h, v)
            else:
                self.end_headers()
            self.wfile.write(response.body)

        def do_GET(self):
            self.do('get')

        def do_POST(self):
            self.do('post')

    def method_decorator(self, method: str):
        def method_handler(path: str):
            def decorator(handler):
                def wrapper(
                    request: Request,
                    response: Response,
                    *args,
                    **kwargs
                ):
                    handler(request, response, *args, **kwargs)
                    return response

                self.handlers[method][path] = wrapper
                return wrapper
            return decorator
        return method_handler

    def __init__(
        self,
        port: int = 8000,
        path: str = 'localhost'
    ) -> None:
        self.address = (path, port)
        self.handlers = {'get': {}, 'post': {}}
        self.get = self.method_decorator('get')
        self.post = self.method_decorator('post')

    def start(self):
        self.Handler.app = self
        server = HTTPServer(self.address, self.Handler)

        try:
            print("i'm alive")
            server.serve_forever()
        except KeyboardInterrupt:
            print("i'm dying")
            server.server_close()
            print("xP")
