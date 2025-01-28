from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Callable


class Request:
    pass


class Response:
    response_code: int
    headers: dict[str, str]
    body: bytes

    def __init__(self) -> None:
        pass

    def json(
        self,
        response_code,
        body: str | bytes,
        headers: dict[str, str] | None = None,
        encoding: str = "utf-8"
    ):
        self.response_code = response_code

        if headers:
            self.headers |= headers
            self.headers.update(headers)

        if isinstance(body, str):
            body = bytes(body, encoding=encoding)
        self.body = body


class Application:
    handlers: dict[str, Callable]
    address: tuple[str, int]

    class Handler(BaseHTTPRequestHandler):
        def do(self):
            pass

        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()

            self.wfile.write(b"{\"hello\": \"world\"}")

    def get(self, path: str):
        def decorator(handler):
            def wrapper(request: Request, response: Response, *args, **kwargs):
                self.handlers[path] = wrapper
                handler(*args, **kwargs)

            return wrapper
        return decorator

    def __init__(
            self,
            port: int = 8000,
            path: str = 'localhost'
    ) -> None:
        self.address = (path, port)
        self.handlers = {}

    def start(self):
        server = HTTPServer(self.address, self.Handler)

        try:
            print("server started")
            server.serve_forever()
        except KeyboardInterrupt:
            print("i'm dying")
            server.server_close()
            print("xP")
