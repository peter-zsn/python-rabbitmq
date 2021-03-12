# coding: utf-8
"""
@auther: 张帅男
@data: 2021/3/12 上午9:46
@文件名字：ramq_pool.py
"""

import pika
import threading
import random
import uuid


class RabbitmqPool:
    __instance = None
    __lock = threading.Lock()

    def __init__(self, connectionsize, channelsize):
        self.maxconnectionsize = connectionsize
        self.maxchannelsize = channelsize
        self.nowconnectionsize = 0
        self.nowchannelsize = 0
        self.connectionpool = {}
        self.channelpool = {}
        self.certdict = {}

    def __new__(cls, connectionsize, channelsize):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def get_channel(self):
        try:
            self.__lock.acquire()
            cname = ""
            channel = None
            for connectionname in self.connectionpool:
                if len(self.channelpool[connectionname]) != 0:
                    channel = self.channelpool[connectionname][-1]
                    cname = connectionname
                    self.channelpool[connectionname] = self.channelpool[connectionname][0:-1]
                    break
            if cname == "":
                if self.nowchannelsize < self.maxchannelsize:
                    if len(self.connectionpool) != 0:
                        cname = random.choice(list(self.connectionpool))
                        # 根据名字拿到此连接，传入连接和Pool池创建Channel
                        CreateChannel(self.connectionpool[cname], self)
                        # 得到一个新Channel
                        channel = self.channelpool[cname][-1]
                        self.channelpool[cname] = self.channelpool[cname][0:-1]
                    else:
                        if len(self.certdict) != 0:
                            cert = random.choice(list(self.certdict))
                            cname = str(uuid.uuid4().int)
                            print("创建一个连接")
                            CreateConnection(str(self.certdict[cert]["rabbitmq_host"]),
                                             str(self.certdict[cert]["rabbitmq_port"]),
                                             str(self.certdict[cert]["rabbitmq_virtual_host"]),
                                             str(self.certdict[cert]["rabbitmq_user"]),
                                             str(self.certdict[cert]["rabbitmq_password"]), self, cname)
                            CreateChannel(self.connectionpool[cname], self)
                            # 得到一个新Channel
                            channel = self.channelpool[cname][-1]
                            self.channelpool[cname] = self.channelpool[cname][0:-1]
                            print("创建一个Channel")
                        else:
                            print("无法创建Channel,无连接凭证,不能创建连接！")
            else:
                print('无法创建，超过限制')
        finally:
            self.__lock.release()
        return channel, cname

    def create_channel(self):
        try:
            self.__lock.acquire()
            if len(self.certdict) != 0:
                cert = random.choice(list(self.certdict))
                cname = str(uuid.uuid4().int)
                CreateConnection(
                    str(self.certdict[cert]["rabbitmq_host"]),
                    str(self.certdict[cert]["rabbitmq_port"]),
                    str(self.certdict[cert]["rabbitmq_virtual_host"]),
                    str(self.certdict[cert]["rabbitmq_user"]),
                    str(self.certdict[cert]["rabbitmq_password"]),
                    self,
                    cname
                )
                CreateChannel(self.connectionpool[cname], self)
                channel = self.channelpool[cname][-1]
                self.channelpool[cname] = channel
                return channel, cname
            else:
                print('没有链接凭证，无法创建')
            return None
        finally:
            self.__lock.release()

    def return_channel(self, channel, connectionname):
        try:
            self.__lock.acquire()
            self.channelpool[connectionname].append(channel)
        finally:
            self.__lock.release()

    def delconnection(self, connectionname):
        try:
            self.__lock.acquire()
            if connectionname in self.connectionpool:
                del self.connectionpool[connectionname]
                self.nowconnectionsize -= 1
                self.nowchannelsize = self.nowchannelsize - len(self.channelpool[connectionname])
                del self.channelpool[connectionname]
        finally:
            self.__lock.release()

    def addcert(self, cert):
        self.certdict[cert["rabbitmq_host"]] = cert

    def get_certtemplate(self):
        return {"rabbitmq_host": "", "rabbitmq_port": 0, "rabbitmq_virtual_host": "", "rabbitmq_user": "",
                "rabbitmq_password": ""}


class CreateConnection:
    def __init__(self, rabbitmq_host, rabbitmq_port, rabbitmq_virtual_host,
                 rabbitmq_user, rabbitmq_password, RabbitmqPool,
                 Connectionname = str(uuid.uuid4().int), heartbeat=60):
        if RabbitmqPool.nowconnectionsize < RabbitmqPool.maxconnectionsize:
            if Connectionname not in RabbitmqPool.connectionpool:
                self.rabbitmq_user = str(rabbitmq_user)
                self.rabbitmq_password = str(rabbitmq_password)
                self.rabbitmq_host = rabbitmq_host
                self.rabbitmq_port = rabbitmq_port
                self.rabbitmq_virtual_host = rabbitmq_virtual_host
                self.Connectionname = Connectionname
                credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
                try:
                    self.connection = pika.BlockingConnection(
                        pika.ConnectionParameters(
                            host=rabbitmq_host,
                            port=rabbitmq_port,
                            virtual_host=rabbitmq_virtual_host,
                            credentials=credentials,
                            heartbeat=heartbeat))
                    RabbitmqPool.connectionpool[Connectionname] = self
                    RabbitmqPool.nowconnectionsize += 1
                    if self.Connectionname not in RabbitmqPool.channelpool:
                        RabbitmqPool.channelpool[Connectionname] = []
                except Exception as e:
                    print('创建链接失败', e)
            else:
                print('链接名字已经存在，创建失败', Connectionname)
        else:
            print('连接池已满， 无法新建链接')

    def get_connection(self):
        return self.connection


class CreateChannel:
    def __init__(self, Connection, RabbitmqPool):
        RabbitmqPool.channelpool[Connection.Connectionname].append(Connection.get_connection().channel())
        RabbitmqPool.nowchannelsize += 1