import sys
from .streamer import Streamer

def main():
    streamer = Streamer()
    streamer.run()

if __name__ == '__main__':
    main()