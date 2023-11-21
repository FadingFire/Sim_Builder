from bluesky.network.client import Client


class TextClient(Client):
    def __init__(self):
        super().__init__()

    def stack(self, text):
        self.send_event(b'STACK', text, b"*")


bsclient = TextClient()


def connectbs():
    bsclient.connect(event_port=11000, stream_port=11001)
