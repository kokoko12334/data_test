import KafkaPro
from multiprocessing import Process
import logging
import sys
import time
import os
from multiprocessing import Process

msg = b'a'*4096
num = 1000000

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def req(msg,num,b,t):
    broker, topic = b,t
    p_id = os.getpid()    
    message_producer = KafkaPro.MessageProducer(broker, topic)
    logging.info(f"broker: {broker}, topic: {topic}, msg_size:{sys.getsizeof(msg)}, num:{num}")

    for _ in range(num):
        res = message_producer.send_message(msg)
        logging.info(f"PID:{p_id}, data: {res}")         


if __name__ == "__main__":

    s = time.time()   

    topics= ['test1','test2','test3','test4','test5']
    process_num = len(topics)
    
    processes = []
    for i in range(process_num):

        process = Process(target=req, args=(msg,num,'34.146.29.164:29092',topics[i]))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    e = time.time()
    logging.info(f"time:{e-s}")