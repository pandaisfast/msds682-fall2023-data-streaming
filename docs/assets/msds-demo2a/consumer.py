"""
Jeremy Gu

This script is a modified version of the Python Kafka consumer found at:
https://developer.confluent.io/courses/apache-kafka/consumers-hands-on/

Modifications and additional comments were added to make it better suited for our teaching purposes.
"""

# Import necessary modules
from argparse import ArgumentParser, FileType
from configparser import ConfigParser
from confluent_kafka import Consumer

# Function to decode messages that might be in bytes
# Extra credit: What if  Kafka message being consumed contains non-UTF-8 encoded content? 
# def decode_message(msg_content):
#     """Decode message content from bytes to string if necessary.

#     Args:
#         msg_content (bytes or str): The content of the message, either in bytes or string format.

#     Returns:
#         str: Decoded message content in string format.
#     """
#     try:
#         return msg_content.decode('utf-8')
#     except AttributeError:
#         return None

def decode_message(msg_content):
    try:
        return msg_content.decode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        # Handle non-textual/binary data or other decoding errors.
        # Here we're just returning a string indicating an error,
        # but you can implement more specific handling if needed.
        return "<UNDECODABLE MESSAGE>"

# The main execution of the script starts here
if __name__ == '__main__':
    # Set up command-line argument parsing
    parser = ArgumentParser(description="Consume messages from Kafka")
    parser.add_argument('config_file', type=FileType('r'), help="Path to the config file")
    parser.add_argument('topic', type=str, help="Kafka topic to consume from")
    args = parser.parse_args()


    # Read the external configuration file
    config_parser = ConfigParser()
    config_parser.read_file(args.config_file)
    config = dict(config_parser['default'])
    config.update(config_parser['consumer'])

    # Initialize the Kafka Consumer with the parsed configuration
    consumer = Consumer(config)

    # Subscribe to a specific Kafka topic, in this case, "demo1_free_text"
    # topic = "demo1_free_text"
    consumer.subscribe([args.topic])

    # Continuous polling loop to check and retrieve new messages from the subscribed Kafka topic
    try:
        while True:
            # Poll for a new message. Wait for a maximum of 1 second.
            msg = consumer.poll(1.0)
            
            # If no message is retrieved in the given time, print "Waiting..."
            if msg is None:
                print("Waiting...")
            
            # If there's an error while polling, print the error message
            elif msg.error():
                print("ERROR: {}".format(msg.error()))
            
            # If a message is successfully retrieved, decode and print its content
            else:
                key = decode_message(msg.key())
                value = decode_message(msg.value())
                print(f"Consumed event from topic {msg.topic()}: key = {key:12} value = {value:12}")

    # Exit the polling loop gracefully upon receiving a keyboard interrupt (e.g., Ctrl+C)
    except KeyboardInterrupt:
        pass
    
    # Ensure that the consumer connection is closed properly before exiting the script
    finally:
        consumer.close()