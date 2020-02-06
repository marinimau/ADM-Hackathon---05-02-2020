# [ADM] Hackathon 05-02-2020

## Description

The system simulates the VISA-transaction data management  for analytics. It must receive data from an input data stream (Main.py) that simulates data arrival. The data must be distributed to two types of clients:
- An internal analysis team: they can perform geographical queries or use a GIS interface (like Q-GIS)
- External analysis companies: these companies need data streams composed by one or more shop categories based on their interests. 

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

### KAFKA *** change IP address

Start zookeeper:    
```
zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties
```

Start server Kafka:     
```
kafka-server-start /usr/local/etc/kafka/server.properties
```

Create topic:    
```
kafka-topics --create --zookeeper 192.168.1.28:2181 --replication-factor 1 --partitions 1 --topic nome_topic
```

Console del produttore:  
```
kafka-console-producer​ --broker-list 192.168.1.28:9092 --topic​ nome_topic
```

Console del consumatore:   
```
kafka-console-consumer --bootstrap-server 192.168.1.28:9092 --topic nome_topic —from-beginning
```

Start producer script:    
```
/Users/mauromarini/Documents/code_kafka_changestreams/kafkaproducer.py
```

Start consumer script:    
```
python /Users/mauromarini/Documents/code_kafka_changestreams/kafkaconsumer.py
```

### Create these 2 topics statically:

```
data_in
```
```
mongo_in
```


### Configure PostegreSQL:

You can find the instrcutions in the following file:
```
./SQL/postegre_creation.sql
```


### Start Python scripts following this order:

1. Main.py from its folder (this simulate data arrival)
2. postgresql.postgreconsumer.py (to read the Kafka stream)
3. postegresql.analysis_society.py (to use the raw interface to execute 3 given queries)
4. mongo_router.router.py (to classify the input stream into shop_category topics)
5. mongo_router.receive_interests (to load into mongo db the given_user stream)


## Team

[Mauro Marini](https://github.com/marinimau)

[Giacomo Balloccu](https://github.com/giacoballoccu)
