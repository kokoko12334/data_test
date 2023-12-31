from kafka import KafkaConsumer
import logging
import sys
from threading import Thread
import time
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


brokers = [i for i in input("brokers: ").split(",")]
g_id = input("그룹이름:")

consumer_config = {
    'bootstrap_servers': brokers,
    'group_id': g_id,
    'auto_offset_reset': 'earliest',
    'enable_auto_commit': True,
    'consumer_timeout_ms': 20000,
    'max_partition_fetch_bytes':1024*1024*16,
    'session_timeout_ms':70000,
    # 'fetch_max_bytes':1024*1024*60,
    'max_poll_records': 4000,
    'fetch_min_bytes':1024*1024,
    'fetch_max_wait_ms':100

}

num_consumers = 4

consumers = []
for i in range(num_consumers):
    consumer = KafkaConsumer(**consumer_config)
    consumer.subscribe(['test1','test2','test3','test4'])
    consumers.append(consumer)
    
def consumer_messages(consumer_instance):
    for message in consumer_instance:
        if message:
            
            logging.info(f"topic: {message.topic}, partition:{message.partition}, msg_size:{sys.getsizeof(message.value)}Byte")


if __name__ == "__main__":
 
    threads = []
    for consumer in consumers:
        thread = Thread(target=consumer_messages, args=(consumer,),daemon=True)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
