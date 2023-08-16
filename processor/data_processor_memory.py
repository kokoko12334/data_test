from kafka import KafkaProducer
import logging
from multiprocessing import Process, Value, Manager
import os
import json
import sys
import time


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def receive_and_put(shm,shm_len,p1_idx,p2_idx,num):

    msg = 'a'*4092

    p_id = os.getpid()
    
    while p1_idx.value < num:

        idx = (p1_idx.value+1)%shm_len
        
        if idx == (p2_idx.value%shm_len):
            
            pass
        
        else:

            shm[idx] = msg

            logging.info(f"PID:{p_id}, receive and put:{sys.getsizeof(msg)}byte, {p1_idx.value}번째 데이터 보냄")

            p1_idx.value = p1_idx.value + 1

    return

def get_and_send(shm,shm_len,p1_idx,p2_idx,num):

    broker = "34.146.29.164:29092"

    producer = KafkaProducer(
                        bootstrap_servers=broker,
                        value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                        acks=1,
                        batch_size = 1024*1024,
                        linger_ms=100,
                        #buffer_memory= 1024*1024*5,
                        max_request_size=1024*1024*1024,
                        # compression_type='snappy',
                        )
    
    topic = "test1"

    p_id = os.getpid()

    while p2_idx.value < num:

        if p2_idx.value == p1_idx.value:

            pass

        else:

            p2_idx.value = p2_idx.value + 1

            idx = p2_idx.value%shm_len

            msg = shm[idx]

            producer.send(topic, msg)

            logging.info(f"PID:{p_id}, get and send:{sys.getsizeof(msg)}byte")  
    
    return




if __name__=="__main__":

    with Manager() as manager:
    
        p1_idx = Value('i', 0)  # 공유메모리 인덱스
        p2_idx = Value('i',0)

        shm_len = 100
        shm = manager.list(['0']*shm_len) 


        num = 10000
        process1 = Process(target=receive_and_put, args=(shm,shm_len,p1_idx,p2_idx,num))
        process2 = Process(target=get_and_send, args=(shm,shm_len,p1_idx,p2_idx,num))

        s = time.time()

        process1.start()
        process2.start()

        process1.join()
        process2.join()

        print(f'총 소요시간:{time.time()-s}')

    