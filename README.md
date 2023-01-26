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