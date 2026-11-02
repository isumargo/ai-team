#!/usr/bin/env python3
"""
serve_status.py — server statis kecil untuk dashboard Status Tim AI.

Menyajikan dua hal di 127.0.0.1:9200:
  /            -> guardian/dashboard/index.html   (kode, ada di repo)
  /team.json   -> workspace/05-status/team.json  (runtime, di-ignore git)

nginx meneruskan ke sini dan memegang TLS + basic auth.

Kenapa server sendiri (bukan alias nginx):
  - /root/ai-team ada di /root yang mode 700; worker nginx (www-data) tidak
    bisa traverse. Service ini jalan sebagai root, konsisten dengan pola
    vhost distro yang sudah ada.
  - Dashboard HTML dan runtime JSON berada di dua tempat berbeda, jadi butuh
    routing kecil (bukan sekadar static root).

Keamanan:
  - Bind HANYA ke 127.0.0.1. Tidak pernah 0.0.0.0.
  - Basic auth ditegakkan di layer nginx (auth_basic_user_file), sama seperti
    vhost distro & mission-control. Modul 'crypt' dihapus di Python 3.13+,
    jadi verifikasi hash tidak dilakukan di sini.
  - Hanya 3 path yang boleh: '/', '/index.html', '/team.json'.
"""
import http.server
import socketserver
from pathlib import Path

DASHBOARD = Path("/root/ai-team/guardian/dashboard/index.html")
STATUS_JSON = Path("/root/ai-team/workspace/05-status/team.json")
HOST = "127.0.0.1"
PORT = 9200

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".json": "application/json; charset=utf-8",
}


class Handler(http.server.BaseHTTPRequestHandler):
    server_version = "team-status"

    def _resolve(self):
        """-> (path_servable, content_type) atau None kalau path tidak diizinkan."""
        path = self.path.split("?", 1)[0]
        if path in ("/", "/index.html"):
            return DASHBOARD, "text/html; charset=utf-8"
        if path == "/team.json":
            return STATUS_JSON, "application/json; charset=utf-8"
        return None

    def _serve(self, head_only=False):
        target = self._resolve()
        if target is None:
            self.send_error(404)
            return
        path, ctype = target
        try:
            body = path.read_bytes()
        except OSError:
            self.send_error(503, "Status belum tersedia")
            return
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if not head_only:
            self.wfile.write(body)

    def do_GET(self):
        self._serve(head_only=False)

    def do_HEAD(self):
        self._serve(head_only=True)

    def log_message(self, format, *args):
        print(f"[team-status] {self.address_string()} {format % args}", flush=True)


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    if not DASHBOARD.exists():
        raise SystemExit(f"Dashboard tidak ditemukan: {DASHBOARD}")
    with Server((HOST, PORT), Handler) as httpd:
        print(
            f"[team-status] serving {DASHBOARD} + {STATUS_JSON} "
            f"di http://{HOST}:{PORT}",
            flush=True,
        )
        httpd.serve_forever()


if __name__ == "__main__":
    main()
