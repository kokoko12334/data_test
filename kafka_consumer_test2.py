from confluent_kafka import Consumer, KafkaError
import logging
import sys
from threading import Thread
import time
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

broker = input("brokers: ")
g_id = input("그룹이름:")
# Kafka Consumer 설정
conf = {
    'bootstrap.servers': broker,
    'group.id': g_id,
    'auto.offset.reset': 'latest',
    'enable.auto.commit': True,
    'allow.auto.create.topics':False,
    'max.partition.fetch.bytes':1024*1024*16,
    'session.timeout.ms':70000,   #heartbeat를 기다리는 시간, 설정한 시간을 넘어버리면 리밸런싱함(default:10초)
    'message.max.bytes':1024*1024*60,
    'fetch.min.bytes':1024*1024,
    # 'max.poll.interval.ms':1000, #다음 poll까지 기다리는 시간, 이 시간 설정을 넘겨도 poll하지 않으면 리밸런싱함
    'heartbeat.interval.ms':3000, #살아있다는 heartbeat를 주는 주기(default:3초)
    # 'max.poll.records':2000
}

num_consumers = 4

consumers = []
for i in range(num_consumers):
    consumer = Consumer(conf)
    consumers.append(consumer)


topics=['test1','test2']
def basic_consume_loop(consumer, topics):
    running = True
    logging.info(f"상태: 실행 중")
    poll_timeout = 1
    try:
        consumer.subscribe(topics)

        while running:
            msg = consumer.poll(timeout=poll_timeout)
            if msg is None:
                timeout = 20  # 20초간 데이터가 없으면 종료
                flag = True
                start_time = time.time()
                while (time.time() - start_time) < timeout:
                    msg = consumer.poll(timeout=poll_timeout)
                    if msg is not None:
                        logging.info(f"topic: {msg.topic()}, partition:{msg.partition()}, msg_size:{sys.getsizeof(msg.value())}Byte")
                        flag = False
                        break  # 데이터가 들어오면 종료하지 않음
                    
                if flag:
                    print(f"No messages received in the last {timeout} seconds. Exiting...")
                    running = False
                    consumer.close()
                    break  # timeout 동안 데이터가 없으면 종료

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                     (msg.topic(), msg.partition(), msg.offset()))
                
            else:
                logging.info(f"topic: {msg.topic()}, partition:{msg.partition()}, msg_size:{sys.getsizeof(msg.value())}Byte")

    finally:
        # Close down consumer to commit final offsets.
        consumer.close()



if __name__ == "__main__":
 
    threads = []
    for consumer in consumers:
        thread = Thread(target=basic_consume_loop, args=(consumer,topics),daemon=True)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()