import pika

class Stock:
    def __init__(self, callback) -> None:
        self.__host = "localhost"
        self.__port = 5672
        self.__username = "guest"
        self.__password = "guest"
        self.__queue = "data_queue"
        self.__exchange = ""
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
            queue=self.__queue,
            auto_ack=True,
            on_message_callback=self.__callback
        )

        return channel
    
    def start(self):
        print(f'Listening RabbitMQ on Port 5672')
        self.__channel.start_consuming()

def minha_callback(ch, method, properties, body):
    estoque_ok = False
    # Lógica de verificação de estoque...
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='estoque_confirmado', durable=True)
    channel.queue_declare(queue='estoque_insuficiente', durable=True)

    evento_resposta = 'estoque_confirmado' if estoque_ok else 'estoque_insuficiente'
    print('Pedido recebido!')
    print('Dados do pedido:' + str(body))
    print('Enviando dados para a fila: ' + evento_resposta)
    channel.basic_publish(exchange="", routing_key=evento_resposta, body="")

rabitmq_consumer = Stock(minha_callback)
rabitmq_consumer.start()