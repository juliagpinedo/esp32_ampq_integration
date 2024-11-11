"""consumer.py"""
import pika
import serial

class Consumer:
    """
    Esta clase representa a un consumidor de mensajes que recibe operaciones
    matemáticas de la cola "display_queue", calcula el resultado y lo envía
    a la ESP32 a través del puerto serial.
    """

    def __init__(self, url, port, baudrate=115200, queue_name='display_queue'):
        """
        Inicializador

        Args:
            url (str): URL de conexión a CloudAMQP
            port (str): Puerto serial al que está conectada la ESP32
            baudrate (int): Velocidad de baudios para la conexión serial.
                            Default a 115200
            queue_name (str): Nombre de la cola que el consmidor
                              escucha. Default a "display_queue"
        """
        self.connection = pika.BlockingConnection(pika.URLParameters(url))
        self.channel = self.connection.channel()
        self.queue_name = queue_name
        self.channel.queue_declare(queue=self.queue_name)
        self.serial_connection = serial.Serial(port=port, baudrate=baudrate)

    @staticmethod
    def calculate(expression):
        """
        Evalúa de forma segura una expresión matemática y retorna el resultado

        Args:
            expression (str): La expresión matemática a evaluar

        Returns:
            str: El resultado de la expresión o un mensaje de error
                 (según aplique)
        """
        try:
            result = eval(expression, {"__builtins__": None}, {})
            if isinstance(result, float) and result.is_integer():
                return str(int(result))
            elif isinstance(result, float):
                return f"{result:.2f}"
            else:
                return str(result)
        except ZeroDivisionError:
            return "Error: Division by zero"
        except Exception as e:
            return f"Error: {e}"

    def callback(self, ch, method, properties, body):
        """
        Función de callback que procesa cada mensaje recibido

        Args:
            ch (pika.Channel): El canal de comunicación con RabbitMQ
            method (pika.spec.Basic.Deliver): Información sobre la entrega del mensaje
            properties (pika.spec.BasicProperties): Propiedades del mensaje
            body (bytes): El mensaje recibido, que contiene la expresión matemática
        """
        expression = body.decode()
        result = self.calculate(expression)
        print(f'[Consumer] Resultado de la operación: {result}')
        self.serial_connection.write(result.encode())

    def run(self):
        """
        Configura el consumidor para que escuche mensajes en el queue "display_queue"
        y procesa cada mensaje con "callback"

        Returns:
            None
        """
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)
        print('[Consumer] Esperando operaciones...')
        self.channel.start_consuming()

    def close_connection(self):
        """
        Cierra las conexiones de CloudAMQP y el puerto serial

        Returns:
            None
        """
        self.connection.close()
        self.serial_connection.close()

if __name__ == "__main__":
    # Inicializa el consumidor con la URL de CloudAMQP y el puerto serial
    amqp_url = 'amqps://pcqakcar:uZ8KkoF2kAiIkAUt4oAJjfEKc-JkZB2D@gull.rmq.cloudamqp.com/pcqakcar'
    serial_port = 'COM3'
    consumer = Consumer(amqp_url, serial_port)
    consumer.run()
