"""producer.py"""
import pika

class Producer:
    """
    Esta clase representa a un productor de mensajes que envía
    operaciones matemáticas a la cola 'display_queue' de CloudAMQP.
    """
    def __init__(self, url, queue_name='display_queue'):
        """
        Inicializador

        Args:
            url (str): URL de conexión a CloudAMQP
            queue_name (str): Nombre de la cola a la que se publicarán los
                            mensajes. Default a "display_queue"
        """
        self.connection = pika.BlockingConnection(pika.URLParameters(url))
        self.channel = self.connection.channel()
        self.queue_name = queue_name
        self.channel.queue_declare(queue=self.queue_name)

    def send_message(self, message):
        """
        Manda un mensaje al queue especificado

        Args:
            message (str): La expresión matemática a enviar
        """
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=message)
        print(f'[Producer] Envio de expresión: {message}')

    def close_connection(self):
        """
        Termina la conexión con el broker CloudAMQP

        Returns:
            None
        """
        try:
            if self.connection.is_open:
                self.connection.close()
        except pika.exceptions.StreamLostError:
            print('Advertencia: la conexión ya estaba cerrada o se interrumpió')

    def run(self):
        """
        Ejecuta el producer al preguntar al usuario por una operación matemática
        válida, y lo envía al queue

        Returns:
            None
        """
        try:
            while True:
                expression = input('Ingrese una operación matemática: ')
                self.send_message(expression)
        except KeyboardInterrupt:
            print('\nInterrupción manual detectada. Cerrando conexión...')
        finally:
            self.close_connection()


if __name__ == "__main__":
    # Inicializar el producer con el URL definido desde CloudAMQP
    amqp_url = 'amqps://pcqakcar:uZ8KkoF2kAiIkAUt4oAJjfEKc-JkZB2D@gull.rmq.cloudamqp.com/pcqakcar'
    producer = Producer(amqp_url)
    producer.run()
