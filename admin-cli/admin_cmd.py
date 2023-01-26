'''
Module to illustrate Kafka and Admin CLI with the help of FastAPI
'''
import logging
from fastapi import FastAPI
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

BOOTSTRAP_SERVERS = "127.0.0.1:9092"
TOPIC_NAME = "ishwar-topic"
app = FastAPI()
logger = logging.getLogger()


@app.on_event("startup")
async def startup_event():
    '''
    This function will run on startup and will create a topic if not existing already.
    '''
    client = KafkaAdminClient(bootstrap_servers=BOOTSTRAP_SERVERS)
    topic = NewTopic(name=TOPIC_NAME, num_partitions=2, replication_factor=1)

    try:
        client.create_topics([topic])

    except TopicAlreadyExistsError:
        logger.warning("Topic already exists")

@app.get('/hello')
async def hello():
    return {"msg": "Hello"}