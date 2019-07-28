import zmq
from threading import Thread
import queue
from client_login import LoginClient


class Client:
    def __init__(self, server_address, server_router_ID, target):
        self.context = zmq.Context.instance()
        self.username = None
        self.server_address = server_address
        self.q = queue.Queue()
        self.message = None
        self.server_router_ID = server_router_ID
        self.target = target

    def run(self):
        self.username = self.login()
        self.main()

        # heartbeat

    def main(self):
        main_socket = self.context.socket(zmq.DEALER)
        main_socket.setsockopt(zmq.IDENTITY, self.username.encode())
        main_socket.connect("tcp://localhost:{}".format(self.server_address))
        print('Client connected!\n')

        relay = ClientRelay(main_socket, self.q, self.target)
        relay.start()
        while True:
            self.message = input('')
            self.q.put(self.message)

    @staticmethod
    def login():
        login = LoginClient('5557')
        return login.login()


class ClientRelay(Thread):
    def __init__(self, main_socket, msg_queue, target):
        self.main_socket = main_socket
        self.msg_queue = msg_queue
        self.target = target
        Thread.__init__(self)

    def run(self):

        while True:
            if self.main_socket.poll(1):
                incoming_message = self.main_socket.recv_json()
                self.message_received(incoming_message)
            if not self.msg_queue.empty():
                client_message = self.msg_queue.get()
                data = {'to': self.target,
                        'message': client_message}

                self.main_socket.send_json(data)

    def message_received(self, incoming_message):
        ID = incoming_message['id']
        if ID==self.target:
            new_message = incoming_message['message']
            print('{}: {}'.format(ID, new_message))
        return
