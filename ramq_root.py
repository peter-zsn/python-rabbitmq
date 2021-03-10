# coding: utf-8
"""
@auther: 张帅男
@data: 2021/3/10 上午11:03
@文件名字：ramq_root.py
"""
import pika
from retry import retry
import threading

username = 'admin'
password = '123456'
credentials = pika.PlainCredentials(username, password)        # mq
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='127.0.0.1',
    port=5672,
    credentials=credentials,
    heartbeat=0
))
channel = connection.channel()
result = channel.queue_declare(queue='python-test', durable=True)


def callback(ch, method, properties, body):
    print(f'produ recv %s' % body)


@retry(pika.exceptions.AMQPConnectionError, delay=5, jitter=(1, 3))
def test():
    channel.basic_consume(queue='python-test', on_message_callback=callback, auto_ack=False)
    channel.start_consuming()

if __name__ == "__main__":
    # ts = []
    # for i in range(10):
    #     t = threading.Thread(target=test)
    #     ts.append(t)
    #
    # for t in ts:
    #     t.start()
    #
    # for t in ts:
    #     t.join()
    test()