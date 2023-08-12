import KafkaPro
import threading
import logging
import sys
import time
msg = b'a'*4092

broker = input("broker: ")
topic = input("topic: ")
num = int(input("메세지 수: "))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logging.info(f"broker: {broker}, topic: {topic}, msg_size:{sys.getsizeof(msg)}, num:{num}")

message_producer = KafkaPro.MessageProducer(broker, topic)

def req(msg,num):
    for _ in range(num):
        res = message_producer.send_message(msg)
        logging.info(f"data: {res}")         

if __name__ == "__main__":


    s = time.time()   
    
    req(msg,num)
    
    
    # num_spl = num//3
    # t1 = threading.Thread(target=req, args=(msg,num_spl))
    # t2 = threading.Thread(target=req, args=(msg,num_spl))
    # t3 = threading.Thread(target=req, args=(msg,num_spl))
    # t4 = threading.Thread(target=req, args=(msg,num_spl))

    # t1.start()
    # t2.start()
    # t3.start()
    # t4.start()

    # t1.join()
    # t2.join()
    # t3.join()
    # t4.join()

    e = time.time()
    logging.info(f"time:{e-s}")