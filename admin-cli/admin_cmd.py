'''
Module to illustrate Kafka and Admin CLI with the help of FastAPI
'''
import logging
import uuid
import os
from typing import List
from fastapi import FastAPI
from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError
from fastapi import FastAPI
from faker import Faker
from dotenv import load_dotenv
from kafka.producer import KafkaProducer
from commands import CreatePeopleCommand
from schema import Person
load_dotenv(verbose=True)
BOOTSTRAP_SERVERS = "localhost:9092"
TOPIC_NAME = "ishwar-topic"
app = FastAPI()
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


@app.on_event("startup")
async def startup_event():
    '''
    This function will run on startup and will create a topic if not existing already.
    '''
    client = KafkaAdminClient(bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'])
    topic = NewTopic(name=TOPIC_NAME, num_partitions=1, replication_factor=1)

    try:
        client.create_topics([topic])

    except TopicAlreadyExistsError:
        logger.warning("Topic already exists")

class SuccessHandler:
  def __init__(self, person):
    self.person = person

  def __call__(self, rec_metadata):
    logger.info(f"""
      Successfully produced
      person {self.person}
      to topic {rec_metadata.topic}
      and partition {rec_metadata.partition}
      at offset {rec_metadata.offset}""")


class ErrorHandler:
  def __init__(self, person):
    self.person = person

  def __call__(self, ex):
    logger.error(f"Failed producing person {self.person}", exc_info=ex)


@app.get('/hello')
async def hello():
    return {"msg": "Hello"}
def make_producer():
  producer = KafkaProducer(bootstrap_servers=os.environ['BOOTSTRAP_SERVERS'],
                          linger_ms=int(os.environ['TOPICS_PEOPLE_ADV_LINGER_MS']),
                          retries=int(os.environ['TOPICS_PEOPLE_ADV_RETRIES']),
                          max_in_flight_requests_per_connection=int(os.environ['TOPICS_PEOPLE_ADV_INFLIGHT_REQS']),
                          acks=os.environ['TOPICS_PEOPLE_ADV_ACK'])
  return producer


@app.post('/api/people', status_code=201, response_model=List[Person])
async def create_people(cmd: CreatePeopleCommand):
  people: List[Person] = []
  faker = Faker()
  producer = make_producer()

  for _ in range(cmd.count):
    person = Person(id=str(uuid.uuid4()), name=faker.name(), title=faker.job().title())
    people.append(person)
    a = producer.send(topic=os.environ['TOPICS_PEOPLE_ADV_NAME'],
                key=person.title.lower().replace(r's+', '-').encode('utf-8'),
                value=person.json().encode('utf-8'))\
            .add_callback(SuccessHandler(person))\
            .add_errback(ErrorHandler(person))
    logger.info(a)

  producer.flush()

  return people

