from kafka import KafkaConsumer

broker = "localhost:29092"
topic = "StockPrices"

consumer = KafkaConsumer(
    topic,
    bootstrap_servers=[broker],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
)


for message in consumer:
    print(message.topic, message.partition, message.offset, message.key, message.value)