# coding: utf-8
"""
@auther: 张帅男
@data: 2021/3/10 上午10:44
@文件名字：ramq_produ.py
生产者
"""
import pika
import threading
import time




def test(i):
    username = 'admin'
    password = '123456'
    credentials = pika.PlainCredentials(username, password)  # mq
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='127.0.0.1',
        port=5672,
        virtual_host='/',
        credentials=credentials,
        heartbeat=0
    ))

    channel = connection.channel()
    channel.queue_declare(queue='python-test', durable=True)
    message = f'this is message id : {str(i)}'
    channel.basic_publish(exchange='', routing_key='python-test', body=message)
    channel.close()
    connection.close()

if __name__ == "__main__":
    ts = []
    for i in range(10):
        t = threading.Thread(target=test, args=(i, ))
        ts.append(t)
        # test(i)
    #
    for t in ts:
        t.start()

    for t in ts:
        t.join()

    # connection.close()