import pika
from flask import Flask, request, render_template_string, flash
from order import Order  
import json

class Notification:
    def __init__(self, callback1, callback2) -> None:
        self.__host = "localhost"
        self.__port = 5672
        self.__username = "guest"
        self.__password = "guest"
        self.__queue1 = "estoque_confirmado"
        self.__queue2 = "estoque_insuficiente"
        self.__callback1 = callback1
        self.__callback2 = callback2
        self.__channel = self.__create_channel()

    def __create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username,
                password=self.__password
            )
        )

        channel = pika.BlockingConnection(connection_parameters).channel()
        channel.queue_declare(
            queue=self.__queue1,
            durable=True
        )

        channel.queue_declare(
            queue=self.__queue2,
            durable=True
        )

        channel.basic_consume(
            queue=self.__queue1,
            auto_ack=True,
            on_message_callback=self.__callback1
        )

        channel.basic_consume(
            queue=self.__queue2,
            auto_ack=True,
            on_message_callback=self.__callback2
        )

        return channel
    
    def start(self):
        print(f'Listening RabbitMQ on Port 5672')
        self.__channel.start_consuming()

def estoqueInsuficiente(ch, method, properties, body):
    print(f"Estoque insuficiente!")
    


def estoqueConfirmado(ch, method, properties, body):
    print(f"Estoque confirmado!")



rabitmq_consumer = Notification(estoqueConfirmado, estoqueInsuficiente)
rabitmq_consumer.start()