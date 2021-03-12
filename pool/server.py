# coding: utf-8
"""
@auther: 张帅男
@data: 2021/3/12 上午11:23
@文件名字：server.py
"""
import datetime
from ramq_pool import RabbitmqPool as Pool

rabbitmq_host = "127.0.0.1"
rabbitmq_port = "5672"
rabbitmq_user = "admin"
rabbitmq_password = "123456"
rabbitmq_virtual_host = "/"
Pool = Pool(3, 20)
cert = Pool.get_certtemplate()
cert['rabbitmq_host'] = rabbitmq_host
cert['rabbitmq_virtual_host'] = rabbitmq_virtual_host
cert['rabbitmq_user'] = rabbitmq_user
cert['rabbitmq_password'] = rabbitmq_password
cert['rabbitmq_port'] = rabbitmq_port
Pool.addcert(cert)

def callback(ch, method, properties, body):
    print(f'produ recv %s time is : %s' % (body, datetime.datetime.now()))
    ch.basic_ack(delivery_tag=method.delivery_tag)          # 回复消息，说明本条消息已经消费，请移除queue

channel, cname = Pool.get_channel()
channel.exchange_declare(exchange='pool-test', durable=True, exchange_type='direct')
result = channel.queue_declare(queue='first', durable=True)
channel.queue_bind(exchange='pool-test', queue="first")
channel.basic_consume(queue='first',  on_message_callback=callback)
channel.start_consuming()