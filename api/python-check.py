import json
import os
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    def _send_common_headers(self):
        origin = self.headers.get("Origin")
        allowed_origins = [
            "http://localhost:3000",
            os.environ.get("FRONTEND_ORIGIN"),
        ]

        if origin and origin in allowed_origins:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")

        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-store")

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_common_headers()
        self.end_headers()

    def do_GET(self):
        payload = {
            "ok": True,
            "runtime": "python",
            "service": "chirag-portfolio-api",
            "message": "Python endpoint is running.",
        }

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._send_common_headers()
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))
