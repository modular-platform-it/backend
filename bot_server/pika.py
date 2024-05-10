# Модуль, который отправляет задачи в брокер сообщений (например, RabbitMQ)
import pika


def send_task_to_queue(task_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='bot_tasks')
    channel.basic_publish(exchange='',
                          routing_key='bot_tasks',
                          body=str(task_data))
    connection.close()

# Эта функция может быть вызвана в любом месте бота для отправки задачи
send_task_to_queue({"user_id": 123, "message": "Пример задачи"})