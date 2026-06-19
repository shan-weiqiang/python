"""§6 execution path comparison — pure Python vs C extension."""

class PyConfig:
  def __init__(self, timeout):
    self.timeout = timeout

  def process(self):
    return self.timeout * 2
