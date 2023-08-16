from kafka import KafkaProducer
import logging
from multiprocessing import Process, Pipe
import os
import json
import sys
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def receive_and_put(pipe,num):

    msg = 'a'*4092

    p_id = os.getpid()

    for i in range(num):

        pipe.send(msg)

        logging.info(f"PID:{p_id}, receive and put:{sys.getsizeof(msg)}byte, {i}번째 데이터 보냄")
    

    pipe.send(None)

    pipe.close() 
    
    return

def get_and_send(pipe):

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

    while True:
        
        try:

            msg = pipe.recv()
            
            if msg is None:
                break

            else:
                
                producer.send(topic, msg)
                met = producer.metrics()
                logging.info(f"PID:{p_id}, get and send:{sys.getsizeof(msg)}byte")
            
        except EOFError:
            break  
    
    return




if __name__=="__main__":

    num = 10000

    parent_pipe, child_pipe = Pipe()

    process1 = Process(target=receive_and_put, args=(parent_pipe,num))
    process2 = Process(target=get_and_send, args=(child_pipe,))
    
    s = time.time()

    process1.start()
    process2.start()

    process1.join()
    process2.join()
    
    print(f'총 소요시간:{time.time()-s}')
