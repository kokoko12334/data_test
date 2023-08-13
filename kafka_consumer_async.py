import asyncio
import threading
from aiokafka import AIOKafkaConsumer
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def consume(loop,g_id):
    consumer = AIOKafkaConsumer(
        bootstrap_servers="34.146.29.164:29092",
        loop=loop,
        group_id=g_id,
        auto_offset_reset='latest',
        enable_auto_commit= True,
        session_timeout_ms=70000, 
        fetch_min_bytes=1024*1024,
        heartbeat_interval_ms=3000,
        fetch_max_wait_ms=100,
        consumer_timeout_ms=30000
    )
    topics = ['test1','test2']
    consumer.subscribe(topics)
    await consumer.start()

    try:
        async for msg in consumer:
            logging.info(f"topic: {msg.topic}, partition:{msg.partition}, msg_size:{sys.getsizeof(msg.value)}Byte")                   
    finally:
        await consumer.stop()

def threaded_func(func, *args):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(func(loop, *args))
    loop.close()

if __name__ == "__main__":

    g_id = input("그룹이름:")

    consumer_num = 4
    threads = []
    for _ in range(consumer_num):
        thread = threading.Thread(target=threaded_func, args=(consume, g_id))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()