"""§4.1 pure Python Config class — bytecode execution path."""

class Config:
    def __init__(self, timeout):
        self.timeout = timeout

    def process(self):
        return self.timeout * 2
