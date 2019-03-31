sonosplay
=========

sonosplay is a CLI tool to play an mp3 file or URL on a Sonos speaker

## Instalation

Requirements: Python 3

```bash
git clone https://github.com/drudv/sonosplay
cd sonosplay/
pip install .
```

## How It Works

It creates a streaming HTTP service for the chosen mp3 file and sends a command to a Sonos speaker in your LAN to play the stream. If an URL is passed instead of file name, then no HTTP service is launched and the URL is played right away.

[SoCo library](https://github.com/SoCo/SoCo) is used to communicate with Sonos devices.

## Usage

Once you've installed the tool you can play a file on a Sonos speaker in the network you are connected to:

```bash
sonosplay /path/to/my.mp3
```

Optionally you might specify IP address/port for the sonosplay streaming service or a certain Sonos speaker to play with:

```bash
sonosplay /path/to/my.mp3 --ip 192.168.1.100 --port 8080 --player MyKitchenSpeaker
```

You might also play URL directly without launching a streaming service

```bash
sonosplay https://server.com/path/to/my.mp3
```

## Limitations

Currently the streaming service works forever until a manual stop. Probably we could have some sophisticated logic in further versions to detect when the Speaker finished playing and exit.

## License

[MIT](./LICENSE)
