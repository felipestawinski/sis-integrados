import pika

class Notification:
    def __init__(self, callback) -> None:
        self.__host = "localhost"
        self.__port = 5672
        self.__username = "guest"
        self.__password = "guest"
        self.__queue1 = "estoque_confirmado"
        self.__queue2 = "estoque_insuficiente"
        self.__callback = callback
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
            queue=self.__queue,
            durable=True
        )
        channel.basic_consume(
            queue=self.__queue1,
            auto_ack=True,
            on_message_callback=self.__callback
        )

        channel.basic_consume(
            queue=self.__queue2,
            auto_ack=True,
            on_message_callback=self.__callback
        )

        return channel
    
    def start(self):
        print(f'Listening RabbitMQ on Port 5672')
        self.__channel.start_consuming()

def estoqueInsuficiente(ch, method, properties, body):
    print(f"Estoque insuficiente!")
    print(f"Notificação enviada para o pedido {pedido['id_pedido']}")

def estoqueConfirmado(ch, method, properties, body):
    print(f"Estoque insuficiente!")
    print(f"Notificação enviada para o pedido {pedido['id_pedido']}")

rabitmq_consumer = Notification(minha_callback)
rabitmq_consumer.start()