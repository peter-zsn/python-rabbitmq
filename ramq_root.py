# coding: utf-8
"""
@auther: 张帅男
@data: 2021/3/10 上午11:03
@文件名字：ramq_root.py
"""
import pika
from retry import retry
import threading
import datetime

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
channel.exchange_declare(exchange='python-test', durable=True, exchange_type='fanout')
result = channel.queue_declare(queue='', durable=True)
queue_name = result.method.queue
print(queue_name, 123)
channel.queue_bind(exchange='python-test', queue=queue_name)


def callback(ch, method, properties, body):
    print(f'produ recv %s time is : %s' % (body, datetime.datetime.now()))
    ch.basic_ack(delivery_tag=method.delivery_tag)          # 回复消息，说明本条消息已经消费，请移除queue


def test():
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
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