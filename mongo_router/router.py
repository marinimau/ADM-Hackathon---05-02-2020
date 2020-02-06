from kafka import KafkaConsumer
from kafka import KafkaProducer
from json import loads
from datetime import date
import time
import string
from json import dumps
from kafka.admin import KafkaAdminClient, NewTopic
import re

class Router:

    def route(self):
        consumer = KafkaConsumer(
             'mongo_in',
             bootstrap_servers=['192.168.1.28:9092'],
             auto_offset_reset='earliest',
             enable_auto_commit=True,
             group_id='my-group',
             value_deserializer=lambda x: loads(x.decode('utf-8')))

        for message in consumer:
            topic = self.extract_topic(message)
            topic = self.validate_string(topic)
            self.check_topics(topic)
            self.send_message(topic, message)
        return

    def extract_topic(self, message):
        message = message.value
        lista = [(v) for k, v in message.items()]
        return str(lista[0])

    def validate_string(self, topic):
        topic = re.sub(r'[^\w]','',topic)
        return topic

    def check_topics(self, topic):
        try:
            admin_client = KafkaAdminClient(bootstrap_servers="192.168.1.28:9092", client_id='test')
            topic_list = []
            topic_list.append(NewTopic(name=topic, num_partitions=1, replication_factor=1))
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
            print("topic creato: {}".format(topic))
        except:
            print("topic esistente: {}".format(topic))
        return

    def send_message(self, topic, message):
        producer = KafkaProducer(bootstrap_servers=['192.168.1.28:9092'],
                                 value_serializer=lambda x:
                                 dumps(x).encode('utf-8'))
        message = message.value
        lista = [(v) for k, v in message.items()]
        shopID = str(lista[3])
        shopCategory = str(lista[0])
        longitude = lista[4]
        latitude = lista[5]
        timestamp = lista[1]
        price = float(lista[2])
        #Inserimento nel topic
        data = {'shopID' : shopID, 'shopCategory' : shopCategory, 'longitude' : longitude, 'latitude' : latitude, 'timestamp' : timestamp, 'price': price}
        producer.send(topic, value=data)
        return


router = Router()
router.route()
