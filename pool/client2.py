# coding: utf-8
"""
@auther: 张帅男
@data: 2021/3/12 上午11:42
@文件名字：client.py
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

try:
    channel, cname = Pool.get_channel()
finally:
    Pool.delconnection(cname)
    channel, cname = Pool.get_channel()

channel.exchange_declare(exchange='pool-test', durable=True, exchange_type='fanout')
message = f'this is message id : 123'
channel.basic_publish(exchange='pool-test', routing_key='secend', body=message)