# kafka-python
Detailed overview of APIs provided by Apache Kafka. 

## To run the kafka docker-compose file

```bash
 docker compose -f devops/docker-compose-local.yml up  
```
## To run FastAPI application

```bash
 uvicorn admin_cmd:app --reload
```

### About Kafka
Kafka is a distributed, fault-tolerant, and high-throughput message broker that can be used to collect and process streams of data in real-time. It is often used as a real-time data pipeline to collect and aggregate data from various sources (such as sensors, logs, and user events) and make it available for downstream processing and analytics.

### To check names of topics present in Kafka. Topic is created once you start the FastAPI server. 
``` 
docker exec -it cli-tools kafka-topics --bootstrap-server broker0:29092 --list
docker exec -it cli-tools kafka-topics --bootstrap-server broker0:29092 --describe --topic ishwar-topic
        Topic: ishwar-topic     PartitionCount: 2       ReplicationFactor: 1    Configs: min.insync.replicas=2
        Topic: ishwar-topic     Partition: 0    Leader: 0       Replicas: 0     Isr: 0
        Topic: ishwar-topic     Partition: 1    Leader: 0       Replicas: 0     Isr: 0

```

### To run producer and consumer
```
docker exec -it cli-tools kafka-console-consumer --bootstrap-server broker0:29092 --topic ishwar-topic --from-beginning
docker exec -it cli-tools kafka-console-producer --bootstrap-server broker0:29092 --topic ishwar-topic  
```


```
docker ps
docker logs <container_id>
[main] INFO org.apache.zookeeper.ClientCnxn - zookeeper.request.timeout value is 0. feature enabled=
[main-SendThread(zk:2181)] INFO org.apache.zookeeper.ClientCnxn - Opening socket connection to server zk/172.25.0.3:2181. Will not attempt to authenticate using SASL (unknown error)
[main-SendThread(zk:2181)] INFO org.apache.zookeeper.ClientCnxn - Opening socket connection to server zk/172.25.0.3:2181. Will not attempt to authenticate using SASL (unknown error)
[main-SendThread(zk:2181)] INFO org.apache.zookeeper.ClientCnxn - Socket connection established, initiating session, client: /172.25.0.4:57836, server: zk/172.25.0.3:2181


```

## Topic and Replicas in Kafka

In Apache Kafka, data is organized into topics, and each topic is split into a number of partitions. 

Each partition can have multiple replicas, and one of the replicas is designated as the leader. The other replicas are followers. The leader is responsible for handling write requests and the followers replicate the data from the leader.

In-sync replicas (ISRs) are replicas that are fully caught up to the leader and are able to take over as leader if the current leader goes down. In other words, ISRs are the replicas that are considered "healthy" and able to take over leadership if needed.
