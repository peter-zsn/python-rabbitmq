# python-rabbitmq
python操作rabbitmq生产者消费者

# rabbitmq：
## 功能范围
  存储转发----多个发送者，单个者接收者
  分布式事务----多个发送者，多个接收者
  发布订阅-----多个发送者，多个接收者
  基于内容的路由----多个发送者，多个接收者
  文件传输队列-----多个发送者，多个接收者
  点对点对接-----单个发送者，单个接收者
  
### 术语
  connection 链接
  session  会话
  channel  独立的双向 数据流通道
  client    客户端 生产者
  server   服务端    消费者
  peer    对话双方的任意一方
  header    消息属性
  body      消息体
  content   消息内容---包含在body
  
  exchange  交换器，服务器中的实体，接收生产者发来的消息，并传递给绑定交换机的队列
  exchange type   基于不同路由语义的交换器类
  queue     消息队列----保存消息发送给消费者
  bind      消息队列绑定交换机
  bind key  绑定的名称。一些交换器类型可能使用这个名称作为定义绑定器路由行为的模式。
  routing key 消息头， 交换器可以用这个消息头决定如何路由某条消息，转发路径
  durable  消息持久化，服务器重启数据不丢失
  transient  服务器重启 数据丢失
  persistent  消息保存在磁盘中 当服务器重启时，消息不会丢失
  Non-Persistent 服务器将消息保存在内存中，当服务器重启时，消息可能丢失。
  
  
 ### exchange 调取策略
  
  https://img-blog.csdnimg.cn/20181120161646287.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L2Jlc3RteQ==,size_16,color_FFFFFF,t_70
 
  与exchange type, bind key, routingkey 三者有关
  根据routing key 和 exchange 绑定的queue的binding key分配消息，
  生产者在将消息发送给Exchange的时候，一般会指定一个Routing Key，来指定这个消息的路由规则，而这个Routing Key需要与Exchange Type及Binding Key联合使用才能最终生效。
在Exchange Type与Binding Key固定的情况下（一般这些内容都是固定配置好的），我们的生产者就可以在发送消息给Exchange时，通过指定Routing Key来决定消息流向哪里。

### exchange type 
  #### fanout 订阅|广播
      只是与绑定exchange的queue有关， 与 banding key 和 routing key 无关。 
      交换器收到消息后，分发给所有绑定该交换器的队列中。 速度最快
  
  #### direct 路由
    精确匹配：当消息的Routing Key与 Exchange和Queue 之间的Binding Key完全匹配，如果匹配成功，将消息分发到该Queue。
    只有当Routing Key和Binding Key完全匹配的时候，消息队列才可以获取消  息。Direct是Exchange的默认模式。
    RabbitMQ默认提供了一个Exchange，名字是空字符串，类型是Direct，绑定到所有的Queue
  
  
  ### topic 通配符
    模糊匹配，按照正则表达式进行匹配。
    用消息的Routing Key与 Exchange和Queue 之间的Binding Key进行模糊匹配，如果匹配成功，将消息分发到该Queue。


  ### Header 键值对模式
    不依靠routing key， 通过定义的header进行匹配
    
  ### ack  是否确认消息收到
 
 
 
  
