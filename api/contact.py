import json
import os
import re
import smtplib
from email.message import EmailMessage
from http.server import BaseHTTPRequestHandler

MAX_BODY_BYTES = 16_384
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class handler(BaseHTTPRequestHandler):
    def _headers(self):
        origin = self.headers.get("Origin")
        allowed_origins = {
            "http://localhost:3000",
            os.environ.get("FRONTEND_ORIGIN", ""),
        }
        if origin and origin in allowed_origins:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Type", "application/json; charset=utf-8")

    def _json(self, status, payload):
        self.send_response(status)
        self._headers()
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_OPTIONS(self):
        origin = self.headers.get("Origin")
        allowed_origins = {
            "http://localhost:3000",
            os.environ.get("FRONTEND_ORIGIN", ""),
        }
        if origin and origin not in allowed_origins:
            return self._json(403, {"ok": False, "error": "Origin not allowed."})
        self.send_response(204)
        self._headers()
        self.end_headers()

    def do_POST(self):
        origin = self.headers.get("Origin")
        allowed_origins = {
            "http://localhost:3000",
            os.environ.get("FRONTEND_ORIGIN", ""),
        }
        if origin and origin not in allowed_origins:
            return self._json(403, {"ok": False, "error": "Origin not allowed."})

        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            return self._json(400, {"ok": False, "error": "Invalid request."})
        if content_length <= 0 or content_length > MAX_BODY_BYTES:
            return self._json(413, {"ok": False, "error": "Message is too large."})

        try:
            payload = json.loads(self.rfile.read(content_length))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return self._json(400, {"ok": False, "error": "Invalid request."})
        if not isinstance(payload, dict):
            return self._json(400, {"ok": False, "error": "Invalid request."})

        # Quietly accept honeypot submissions to avoid giving bots useful feedback.
        if str(payload.get("website", "")).strip():
            return self._json(200, {"ok": True})

        name = str(payload.get("name", "")).strip()
        sender = str(payload.get("email", "")).strip()
        message = str(payload.get("message", "")).strip()
        if not name or len(name) > 100:
            return self._json(400, {"ok": False, "error": "Enter a name under 100 characters."})
        if len(sender) > 254 or not EMAIL_PATTERN.fullmatch(sender):
            return self._json(400, {"ok": False, "error": "Enter a valid email address."})
        if not message or len(message) > 5000:
            return self._json(400, {"ok": False, "error": "Message must be under 5,000 characters."})

        smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
        smtp_port = int(os.environ.get("SMTP_PORT", "587"))
        smtp_username = os.environ.get("SMTP_USERNAME")
        smtp_password = os.environ.get("SMTP_APP_PASSWORD")
        recipient = os.environ.get("CONTACT_TO_EMAIL", "tankchirag22@gmail.com")
        if not smtp_username or not smtp_password:
            return self._json(503, {"ok": False, "error": "Email delivery is not configured yet."})

        email = EmailMessage()
        email["Subject"] = "New message from your portfolio"
        email["From"] = smtp_username
        email["To"] = recipient
        email["Reply-To"] = sender
        email.set_content(f"Name: {name}\nEmail: {sender}\n\nMessage:\n{message}")

        try:
            with smtplib.SMTP(smtp_host, smtp_port, timeout=12) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.ehlo()
                smtp.login(smtp_username, smtp_password)
                smtp.send_message(email)
        except (OSError, smtplib.SMTPException) as error:
            self.log_error("Contact email delivery failed: %s", error.__class__.__name__)
            return self._json(502, {"ok": False, "error": "Could not send the message right now. Please try again later."})

        return self._json(200, {"ok": True, "message": "Your message has been sent."})
