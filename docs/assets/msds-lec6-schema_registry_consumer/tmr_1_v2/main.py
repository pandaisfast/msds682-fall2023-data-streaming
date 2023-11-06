import logging
import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI
from faker import Faker

from confluent_kafka import SerializingProducer
from confluent_kafka.admin import AdminClient, NewTopic

from confluent_kafka.serialization import StringSerializer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer


import schemas
from commands import CreatePeopleCommand
from entities import Person

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

load_dotenv(verbose=True)

app = FastAPI()

####
def get_kafka_config():
    return {
        'bootstrap.servers': os.environ['BOOTSTRAP_SERVERS'],
        'security.protocol': os.environ['SECURITY_PROTOCOL'],
        'sasl.mechanisms': os.environ['SASL_MECHANISMS'],
        'sasl.username': os.environ['SASL_USERNAME'],
        'sasl.password': os.environ['SASL_PASSWORD'],
    }

@app.on_event('startup')
async def startup_event():
  client = AdminClient(get_kafka_config())
  topic = NewTopic(os.environ['TOPICS_NAME'],
              num_partitions=int(os.environ['TOPICS_PARTITIONS']),
              replication_factor=int(os.environ['TOPICS_REPLICAS']))
  try:
    futures = client.create_topics([topic])
    for topic_name, future in futures.items():
      future.result()
      logger.info(f"Create topic {topic_name}")
  except Exception as e:
    logger.warning(e)


def make_producer() -> SerializingProducer:
  
    schema_reg_client = SchemaRegistryClient({
        'url': os.environ['schema_registry_url'],
        'basic.auth.user.info': os.environ['basic_auth.user_info']
    })

    avro_serializer = AvroSerializer(schema_reg_client,
                                     schemas.person_value_v1,
                                     lambda person, ctx: person.dict())

    kafka_config = get_kafka_config()
    kafka_config.update({
        'linger.ms': 300,
        'enable.idempotence': 'true',
        'max.in.flight.requests.per.connection': 5,  # Can be adjusted for Confluent Cloud
        'acks': 'all',
        'key.serializer': StringSerializer('utf_8'),
        'value.serializer': avro_serializer,
        # 'partitioner': 'murmur2_random' # This is not required and can be removed.
    })

    return SerializingProducer(kafka_config)


class ProducerCallback:
  def __init__(self, person):
    self.person = person

  def __call__(self, err, msg):
    if err:
      logger.error(f"Failed to produce {self.person}", exc_info=err)
    else:
      logger.info(f"""
        Successfully produced {self.person}
        to partition {msg.partition()}
        at offset {msg.offset()}
      """)


@app.post('/api/people', status_code=201, response_model=List[Person])
async def create_people(cmd: CreatePeopleCommand):
    people: List[Person] = []
    faker = Faker()
    producer = make_producer()

    for _ in range(cmd.count):
        person = Person(name=faker.name(), title=faker.job().title())
        people.append(person)
        producer.produce(topic=os.environ['TOPICS_NAME'],
                        key=person.title.lower().replace(r'\s+', '-'),
                        value=person,
                        on_delivery=ProducerCallback(person))

    producer.flush()

    return people

