from time import sleep
import numpy as np
import time
from json import dumps
from kafka import KafkaProducer


class Main:
    def run_all(self):
        filepath = './nyc_purchases_wgs84.csv'

        producer = KafkaProducer(bootstrap_servers=['192.168.1.28:9092'],
                                 value_serializer=lambda x:
                                 dumps(x).encode('utf-8'))

        with open(filepath) as fp:
            line = fp.readline()
            cnt = 1
            while line:
                timestamp = round(time.time(),3)
                price = round(np.random.normal(200, 100),2)
                delay = np.random.normal(0.01, 0.1)
                sleep(abs(delay))
                line = fp.readline()

                #Convert string into substring for json parsing of kafka
                customerID = line.split(',')[0]
                shopID = line.split(',')[1]
                shopCategory = line.split(',')[2].lower()
                longitude = line.split(',')[3]
                latitude = line.split(',')[4][:-1]

                data = {'customerID' : customerID, 'shopID' : shopID, 'shopCategory' : shopCategory, 'longitude' : longitude, 'latitude' : latitude, 'timestamp' : timestamp, 'price': price}
                producer.send('data_in', value=data)
                producer.send('mongo_in', value=data)
                producer.send('debug', value=data)
                print(str(data))
                sleep(1)

main = Main()
main.run_all()
