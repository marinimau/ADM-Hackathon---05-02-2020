from kafka import KafkaConsumer
from pymongo import MongoClient
from json import loads
from multiprocessing import Process


class ReceiveByInterests:

    def manage_topics(self):
        topic_list = ['debug','bar','bridge','office','subway']
        for topic in topic_list:
            p = Process(target=receive, args=(topic,))
            p.start()
            p.join()
        return

def receive(topic):
    try:
        consumer = KafkaConsumer(
             topic,
              bootstrap_servers=['192.168.1.28:9092'],
              auto_offset_reset='earliest',
              enable_auto_commit=True,
              group_id='my-group',
              value_deserializer=lambda x: loads(x.decode('utf-8')))
        print("current topic: {}".format(topic))
        try:
            client = MongoClient('localhost:27018')
            collection = client.visa.visa
        except:
            print("unable to connect to mongo")
            return

        for message in consumer:
            message = message.value
            collection.insert_one(message)
            print('{} added to {}'.format(message, collection))
    except:
         print("unable to read topic")
    return 0

receiver = ReceiveByInterests()
receiver.manage_topics()
