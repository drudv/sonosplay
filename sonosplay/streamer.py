import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import TCPServer

START_PORT = 9000
END_PORT = 9999

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        return BaseHTTPRequestHandler.do_GET(self)

class Streamer:
    def is_port_in_use(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) == 0

    def find_free_port(self):
        for port in range(START_PORT, END_PORT):
            if not self.is_port_in_use(port):
                return port
        raise Exception('Cannot find a free port to use')

    def detect_ip_addr(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.connect(('<broadcast>', 0))
            ip_addr = s.getsockname()[0]
            s.close()
        except socket.socket_error as error:
            raise Exception('Cannot detect IP address to use')
        return ip_addr

    def run(self, predefined_port=None, predefined_ip_addr=None):
        port = predefined_port or self.find_free_port()
        ip_addr = predefined_ip_addr or self.detect_ip_addr()
        with socketserver.TCPServer((ip_addr, port), RequestHandler) as httpd:
            print("Listening to %s:%d" % (ip_addr, port))
            httpd.serve_forever()

