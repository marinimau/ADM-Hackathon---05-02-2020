# [ADM] Hackathon 05-02-2020

## Architecture

![Architecture](https://github.com/marinimau/ADM-Hackathon---05-02-2020/blob/master/hackathon.png)

## Intructions

### MongoDB

Start server:
```
mongod --port 27018 --dbpath /Users/mauromarini/Documents/hackathon/mongo_data --replSet “hackathon”

```
Connect to server:
```
mongo --port 27018

```
Make the MongoDB node primary (in the mongo shell):  

```
rs.initiate()

```

KAFKA *** change IP address

Start zookeeper:    zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties
Start server Kafka:     kafka-server-start /usr/local/etc/kafka/server.properties
Create topic test:    kafka-topics --create --zookeeper 192.168.1.28:2181 --replication-factor 1 --partitions 1 --topic test
Console del produttore:  kafka-console-producer​ --broker-list 192.168.1.28:9092 --topic​ test
Console del consumatore:   kafka-console-consumer --bootstrap-server 192.168.1.28:9092 --topic test —from-beginning
Start producer script:    /Users/mauromarini/Documents/code_kafka_changestreams/kafkaproducer.py
Start consumer script:    python /Users/mauromarini/Documents/code_kafka_changestreams/kafkaconsumer.py

CREATE THESE 2 TOPICS STATICALLY:

- data_in
- mongo_in


CONFIGURE POSTEGRESQL:

SQL.postegre_creation.sql


START PYTHON SCRIPTS IN THIS ORDER:

1. Main.py from its folder (this simulate data arrival)
2. postgresql.postgreconsumer.py (to read the Kafka stream)
3. postegresql.analysis_society.py (to use the raw interface to execute 3 given queries)
4. mongo_router.router.py (to classify the input stream into shop_category topics)
5. mongo_router.receive_interests (to load into mongo db the given_user stream)


## Team

[Mauro Marini](https://github.com/marinimau)
[Giacomo Balloccu](https://github.com/giacoballoccu)
