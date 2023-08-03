from kafka import KafkaConsumer
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

broker = "localhost:9093"
topic = "test"

consumer = KafkaConsumer(
    topic,
    bootstrap_servers=[broker],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
)

lst = []
for message in consumer:

    lst.append(message.value)
    logging.info(f"topic: {message.topic} partition:{message.partition} data:{len(lst)}")

