import sys
import argparse
from .streamer import Streamer

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='Media file name to play')
    parser.add_argument('--port', type=int, help='Port number to listen on')
    parser.add_argument('--ip', help='IP address to bind to')
    parser.add_argument('--player', help='Sonos player name')
    args = parser.parse_args()
    streamer = Streamer()
    streamer.run(media_file=args.file,
                 predefined_port=args.port,
                 predefined_ip_addr=args.ip,
                 predefined_player_name=args.player)

if __name__ == '__main__':
    main()