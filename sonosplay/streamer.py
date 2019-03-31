import os
import re
import soco
import socket
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import TCPServer

START_PORT = 9000
END_PORT = 9999
STREAM_PATH = '/stream.mp3'  # Sonos player wants this '.mp3' extension


def is_url(file_or_url):
    return re.match('^http[s]?://', file_or_url, flags=re.IGNORECASE)


def create_handler(media_file):
    class CustomRequestHandler(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super(CustomRequestHandler, self).__init__(*args, **kwargs)

        def do_GET(self):
            if self.path == STREAM_PATH:
                try:
                    with open(media_file, 'rb') as file:
                        basename = os.path.basename(media_file)
                        stat = os.fstat(file.fileno())
                        self.send_response(200)
                        self.send_header('Content-Length', str(stat[6]))
                        self.send_header(
                            'Content-Type',
                            'audio/mpeg')
                        self.send_header(
                            'Content-Disposition',
                            'attachment; filename="%s"' % basename)
                        self.end_headers()
                        self.wfile.write(file.read())
                except socket.error as error:
                    print('Connection is closed by peer')
                    pass
                except IOError as error:
                    self.send_response(500)
                    print('I/O error: %s' % (str(error)))
                return
            self.send_error(404)
    return CustomRequestHandler


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

    def get_player(self, predefined_player_name=None):
        players = list(soco.discover())
        if len(players) == 0:
            raise Exception('Cannot find any Sonos player')
        if predefined_player_name is None:
            return players[0]
        try:
            return next(p for p in players
                        if p.player_name == predefined_player_name)
        except StopIteration:
            raise Exception("Player %s doesn't exist" % predefined_player_name)

    def run(self,
            media_file_or_url,
            predefined_port=None,
            predefined_ip_addr=None,
            predefined_player_name=None):
        player = self.get_player(predefined_player_name)
        if is_url(media_file_or_url):
            print('Playing %s...' % media_file_or_url)
            player.play_uri(media_file_or_url)
            return
        if not os.path.isfile(media_file_or_url):
            raise Exception("File %s doesn't exist")
        port = predefined_port or self.find_free_port()
        ip_addr = predefined_ip_addr or self.detect_ip_addr()
        Handler = create_handler(media_file=media_file_or_url)
        with HTTPServer((ip_addr, port), Handler) as httpd:
            stream_url = 'http://%s:%s%s' % (ip_addr, port, STREAM_PATH)
            print('Streaming on %s' % stream_url)
            thread = threading.Thread(target=httpd.serve_forever)
            thread.daemon = True
            thread.start()
            player.play_uri(stream_url)
            thread.join()
