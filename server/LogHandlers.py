import logging

class ServerLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()

    def emit(self, record):
        log_entry = self.format(record)
        print(f"Server: {log_entry}")

        return log_entry

class WebSocketLogHandler(logging.Handler):
    def __init__(self ,socketio ,clients):
        super().__init__()
        self.clients = clients
        self.socketio = socketio

    def emit(self, record):
        log_entry = self.format(record)
        for client in self.clients:
            self.socketio.emit('log_message', {'data': log_entry}, room=client)

fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')