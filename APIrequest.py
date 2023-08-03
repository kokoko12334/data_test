import requests
import KafkaPro
import pickle
import threading
import logging

broker = "localhost:9092"
topic = "test"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

with open("nasdaq_symbol_list", 'rb') as f:
    symbols = pickle.load(f)

message_producer = KafkaPro.MessageProducer(broker, topic)

base_url = "https://api.iex.cloud/v1/data/core/quote/"

def req(s,e):
    for i in range(s,e):
        final_url = base_url + symbols[i] + "?token=pk_9458a38e10dd4d40bfe7c9a106550cc9"

        response = requests.get(final_url)

            
        logging.info(f"code: {response}")
        data = response.json()   
        res = message_producer.send_message(data[0])
        logging.info(f"data: {res}")    
        logging.info(f"index: {i}")        


# while 1:
#     response = requests.get(
#         "https://api.iex.cloud/v1/data/core/quote/aapl?token=pk_9458a38e10dd4d40bfe7c9a106550cc9"
#     )

#     print(response)
#     data = {
#             "companyName":response.json()[0]['companyName'],
#             "price":response.json()[0]['iexRealtimePrice'],
#             "time": response.json()[0]['latestTime']
#             }

#     message_producer = KafkaPro.MessageProducer(broker, topic)

#     res = message_producer.send_message(data)
#     print(res)

if __name__ == "__main__":

    # semaphore = threading.Semaphore(1)

    t1 = threading.Thread(target=req, args=(0,1100))
    t2 = threading.Thread(target=req, args=(1100,2200))
    t3 = threading.Thread(target=req, args=(2200,3370))
    
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

