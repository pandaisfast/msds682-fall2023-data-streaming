## pyconsumer.py

import logging
import os

from dotenv import load_dotenv
from confluent_kafka import DeserializingConsumer
from confluent_kafka.error import KafkaError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer

import schemas
from entities import RideRequest

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

load_dotenv(verbose=True)


def make_consumer() -> DeserializingConsumer:
    schema_registry_url = os.environ['schema_registry_url']
    basic_auth_user_info = os.environ.get('basic_auth.user_info')  # Make sure this environment variable is set in your .env file

    schema_reg_config = {
        'url': schema_registry_url,
        'basic.auth.user.info': basic_auth_user_info
    }
    schema_reg_client = SchemaRegistryClient(schema_reg_config)

    avro_deserializer = AvroDeserializer(
        schema_str=schemas.ride_request_schema,
        schema_registry_client=schema_reg_client,
        from_dict=lambda data, ctx: RideRequest(**data)
    )

    consumer_config = {
        'bootstrap.servers': os.environ['BOOTSTRAP_SERVERS'],
        'security.protocol': os.environ['SECURITY_PROTOCOL'],
        'sasl.mechanisms': os.environ['SASL_MECHANISMS'],
        'sasl.username': os.environ['SASL_USERNAME'],
        'sasl.password': os.environ['SASL_PASSWORD'],
        'key.deserializer': StringDeserializer('utf_8'),
        'value.deserializer': avro_deserializer,
        'group.id': os.environ['CONSUMER_GROUP_ID'],
        'auto.offset.reset': 'earliest',
        'enable.auto.commit': 'false'  # Changed to false to manually commit offsets
    }

    return DeserializingConsumer(consumer_config)


def main():
    logger.info(f"Started Python Avro Consumer for topic {os.environ['TOPICS_NAME']}")

    consumer = make_consumer()
    consumer.subscribe([os.environ['TOPICS_NAME']])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    logger.info('End of partition reached {0}/{1}'
                                .format(msg.topic(), msg.partition()))
                else:
                    logger.error(msg.error())
                continue

            ride_request = msg.value()
            if ride_request is not None:
                logger.info(f"Consumed RideRequest: {ride_request}")
                consumer.commit(message=msg)  # Manually commit the message
    except KeyboardInterrupt:
        logger.info("Consumer interrupted by the user.")
    finally:
        # Close down consumer to commit final offsets.
        consumer.close()
        logger.info("Consumer closed.")

if __name__ == '__main__':
    main()
