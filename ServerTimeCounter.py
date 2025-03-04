import time

class ServerCall:
    def __init__(self,timeout = 10):
        self.timeout = timeout
        self.last_called = None

    def call_function(self):
        self.last_called = time.time()

    def check_if_inactive(self):
        if self.last_called is None:
            return True
    
        current_time = time.time()

        if current_time - self.last_called > self.timeout:
            return True
        else:
            return False
