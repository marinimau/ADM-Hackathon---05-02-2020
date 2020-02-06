from kafka import KafkaConsumer
from json import loads
import psycopg2
from datetime import date
import time

consumer = KafkaConsumer(
     'data_in',
     bootstrap_servers=['192.168.1.28:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))

try:
    conn = psycopg2.connect("dbname=visa user=postgres host='localhost' port='5431' password=postgres")
except:
    print "I am unable to connect to the database"

cur = conn.cursor()

for message in consumer:
    message = message.value
    lista = [(v) for k, v in message.items()]
    customerID = int(lista[6])
    shopID = str(lista[3])
    shopCategory = str(lista[0])
    longitude = lista[4]
    latitude = lista[5]
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(lista[1]))
    price = float(lista[2])
    coordinates = "POINT(%s %s)" % (longitude, latitude)
    cur.execute('INSERT INTO visa.nyc_purchases (c_ID, s_ID, s_category, s_coords, price, p_time) VALUES(%s,%s,%s,ST_GeomFromText(%s, 4326),%s,%s)', (customerID, shopID, shopCategory, coordinates, price, timestamp))
    conn.commit()
    print("Row inserted")
