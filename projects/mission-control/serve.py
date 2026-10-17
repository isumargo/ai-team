#!/usr/bin/env python3
"""Simple HTTP server with API endpoints."""
import http.server
import json
import os
from pathlib import Path

PORT = 8080
WEB_DIR = "/root/ai-team/projects/mission-control/web"
STATUS_DIR = "/root/ai-team/status"


class MissionControlHandler(http.server.SimpleHTTPRequestHandler):
 def __init__(self, *args, **kwargs):
 super().__init__(*args, directory=WEB_DIR, **kwargs)

 def do_GET(self):
 if self.path == "/api/status":
 self.send_response(200)
 self.send_header("Content-type", "application/json")
 self.end_headers()
 status_files = [f for f in Path(STATUS_DIR).glob("*.json")]
 status_data = [json.loads(f.read_text()) for f in status_files]
 self.wfile.write(json.dumps(status_data).encode())
 elif self.path == "/api/set-limit":
 self.send_response(200)
 self.send_header("Content-type", "application/json")
 self.end_headers()
 with open("/root/ai-team/guardian/config.json", "w") as f:
 json.dump({"limit": self.headers["X-Limit"]}, f)
 self.wfile.write(json.dumps({"status": "success"}).encode())
 elif self.path == "/api/check-now":
 self.send_response(200)
 self.send_header("Content-type", "application/json")
 self.end_headers()
 os.system("python3 /root/ai-team/guardian/check_usage.py")
 self.wfile.write(json.dumps({"status": "success"}).encode())
 else:
 super().do_GET()


if __name__ == "__main__":
 os.chdir(WEB_DIR)
 server = http.server.HTTPServer(("0.0.0.0", PORT), MissionControlHandler)
 print(f"Serving on port {PORT}")
 server.serve_forever()