from protobuf.message_pb2 import Response, Request
import pika
import uuid
from PyQt5.QtCore import pyqtSignal, QObject, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget


class RpcClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.request_id = 1
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        self.response = Response()
        self.response.ParseFromString(body)

    def call(self, n, timeout):
        request = Request(
            return_address=self.callback_queue,
            request_id=str(self.request_id),
            proccess_time_in_seconds=timeout,
            request=n
        )

        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='double',
            routing_key='server_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=request.SerializeToString())

        self.request_id += 1

        while self.response is None:
            self.connection.process_data_events(time_limit=None)
        return self.response


fibonacci_rpc = RpcClient()

i = int(input("Введите число: "))
t = int(input('Введите задержку во времени: '))
response = fibonacci_rpc.call(i, t)
print(f"Ответ {response.response}")
