import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

from result import calculate_result

VALID_USER = os.environ.get("APP_USER", "tomsmith")
VALID_PASSWORD = os.environ.get("APP_PASSWORD", "SuperSecretPassword")

LOGIN_PAGE = """<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
<h2>Login Page</h2>
<div id="flash">{message}</div>
<form method="post" action="/login">
<input type="text" id="username" name="username">
<input type="password" id="password" name="password">
<button type="submit">Login</button>
</form>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, content_type="text/html"):
        data = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/login":
            self._send(200, LOGIN_PAGE.format(message=""))
        elif url.path == "/result":
            query = parse_qs(url.query)
            try:
                marks = float(query["marks"][0])
                total = float(query.get("total", ["100"])[0])
            except (KeyError, ValueError):
                marks = total = None
            self._send(200, json.dumps(calculate_result(marks, total)), "application/json")
        else:
            self._send(200, "Result app is running. Try /result?marks=78&total=100 or /login")

    def do_POST(self):
        if urlparse(self.path).path != "/login":
            self._send(404, "Not found")
            return
        length = int(self.headers.get("Content-Length", 0))
        form = parse_qs(self.rfile.read(length).decode())
        user = form.get("username", [""])[0]
        password = form.get("password", [""])[0]
        if user == VALID_USER and password == VALID_PASSWORD:
            self._send(200, LOGIN_PAGE.format(message="You logged into a secure area!"))
        else:
            self._send(200, LOGIN_PAGE.format(message="Your username or password is invalid!"))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Serving on port {port}")
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()
