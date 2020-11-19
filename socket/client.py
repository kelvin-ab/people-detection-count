from websocket import create_connection


def short_lived_connection():
    ws = create_connection("ws://localhost:4040/")
    print("Sending 'Hello Server'...")
    ws.send("Hello, Server")
    print("Sent")
    print("Receiving...")
    result = ws.recv()
    print("Received '%s'" % result)
    ws.close()


if __name__ == '__main__':
    short_lived_connection()
