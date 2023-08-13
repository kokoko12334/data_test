from kafka import KafkaProducer
import json

class MessageProducer:
    broker = ""
    topic = ""
    producer = None

    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic
        self.producer = KafkaProducer(bootstrap_servers=self.broker,
                                    #   value_serializer=lambda x: json.dumps(x).encode('utf-8'),
                                      acks=1,
                                      batch_size = 1024*1024,
                                      linger_ms=500,
                                    #   buffer_memory= 1024*1024*5,
                                      max_request_size=1024*1024*1024,
                                      # compression_type='snappy'
                                
                                      )

    def send_message(self, msg):
        try:
            future = self.producer.send(self.topic, msg)
            # self.producer.flush()   # 비우는 작업
            # future.get(timeout=60)
            met = self.producer.metrics()
            
            record_size_avg = met['producer-metrics']['record-size-avg']
            request_latency_avg = met['producer-metrics']['request-latency-avg']
            io_wait_ratio = met['producer-metrics']['request-latency-avg']
            byte_rate = met['producer-metrics']['byte-rate']
            batch_size_avg = met['producer-metrics']['batch-size-avg']
            
            # print(met.keys())
            return {'record_size_avg':record_size_avg,
                    'byte_rate': byte_rate,
                    'request_latency_avg':request_latency_avg,
                    'io_wait_ratio':io_wait_ratio,
                    'batch_size_avg':batch_size_avg,
                    'status_code': 200}
        except Exception as e:
            print("error:::::",e)
            return e