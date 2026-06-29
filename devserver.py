#!/usr/bin/env python3
"""Dev server for Island Hopper: static files (like `python -m http.server`) PLUS a telemetry sink.

  POST /telemetry   body = JSON  → overwrites telemetry.json in this folder (the phone streams its live
                                   orientation/control state here; Claude reads telemetry.json to debug
                                   without seeing the phone screen).
  GET  /telemetry.json           → the latest posted state (also just a normal static file).

Binds 0.0.0.0 so other devices on the LAN (phone) can reach it. Run via `just dev` (or `python3 devserver.py 8080`).
"""
import os, sys, time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
ROOT = os.path.dirname(os.path.abspath(__file__))
TEL  = os.path.join(ROOT, 'telemetry.json')

class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)
    def end_headers(self):
        # CORS + no-store so polled files (reload.txt / telemetry.json) are always fresh
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()
    def do_OPTIONS(self):
        self.send_response(204); self.end_headers()
    def do_POST(self):
        if self.path.split('?')[0] == '/telemetry':
            n = int(self.headers.get('Content-Length') or 0)
            body = self.rfile.read(n) if n else b'{}'
            try:
                with open(TEL, 'wb') as f: f.write(body)
            except Exception:
                self.send_response(500); self.end_headers(); return
            self.send_response(204); self.end_headers()
        else:
            self.send_response(404); self.end_headers()
    def log_message(self, *a):
        pass   # quiet (telemetry would spam)

if __name__ == '__main__':
    open(TEL, 'a').close()   # ensure it exists so GET never 404s
    print(f"[devserver] static + POST /telemetry on http://0.0.0.0:{PORT}  (root {ROOT})")
    ThreadingHTTPServer(('0.0.0.0', PORT), H).serve_forever()
