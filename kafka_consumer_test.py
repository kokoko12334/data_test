from kafka import KafkaConsumer
import logging
import sys
from threading import Thread
import time
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


brokers = [i for i in input("brokers: ").split(" ")]
g_id = input("그룹이름:")

consumer_config = {
    'bootstrap_servers': brokers,
    'group_id': g_id,
    'auto_offset_reset': 'latest',
    'enable_auto_commit': True,
    'consumer_timeout_ms': 10000,
    'fetch_min_bytes':1024
}

num_consumers = 3

consumers = []
for i in range(num_consumers):
    consumer = KafkaConsumer(**consumer_config)
    consumer.subscribe(('test1','test2'))
    consumers.append(consumer)
    
def consumer_messages(consumer_instance):
    for message in consumer_instance:
        if message:
            logging.info(f"topic: {message.topic}, partition:{message.partition}, msg_size:{sys.getsizeof(message.value)}Bytes")


if __name__ == "__main__":
    threads = []
    for consumer in consumers:
        thread = Thread(target=consumer_messages, args=(consumer,),daemon=True)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

