import zmq

class DataIoT():
    server_ilid: str
    temperature: int
    humidity: int
    voltage: int
    current: int

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://localhost:5558") # conecta no broker local
msg_count = 0

while True:
    print(f"Mensagem {msg_count}:", end=" ")
    message = socket.recv()
    socket.send_string("World")
    print(f"{message}")
    msg_count += 1