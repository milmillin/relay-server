from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from subprocess import STDOUT, check_output
import argparse
import os
import ssl

class Handler(BaseHTTPRequestHandler):
  def __init__(self, request, client_address, server):
    self.pwd = os.getenv('MILUAI_PWD')
    super().__init__(request, client_address, server)

  def do_GET(self):
    query_components = parse_qs(urlparse(self.path).query)
    try:
      print(query_components)
      cmd = query_components["cmd"][0]
      pwd = query_components["pwd"][0]
      print(pwd, self.pwd)
      if pwd != self.pwd:
        raise Exception("wrong password")
      res = check_output(cmd, stderr=STDOUT, timeout=5, shell=True)
      self.send_response(200)
      self.send_header('Content-type','text/plain')
      self.end_headers()
      self.wfile.write(res)
    except Exception as e:
      print(e)
      self.send_response(403)
      self.send_header('Content-type','text/plain')
      self.end_headers()
      self.wfile.write(bytes("denied", "utf-8"))

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("-p", "--port", default=8000, type=int)
  args = parser.parse_args()
  pwd = os.getenv("MILUAI_PWD")
  if pwd is None:
    print("please define MILUAI_PWD environment variable")
    return
  with HTTPServer(('', args.port), Handler) as server:
    print(f"pid: {os.getpid()}")
    server.socket = ssl.wrap_socket(server.socket, certfile=f"{os.path.dirname(__file__)}/server.pem", server_side=True)
    sa = server.socket.getsockname()
    print("Serving HTTP on", sa[0], "port", sa[1], "...")
    server.serve_forever()

if __name__ == "__main__":
  main()
