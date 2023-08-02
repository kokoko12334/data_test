import requests
import KafkaPro

broker = "localhost:29092"
topic = "StockPrices"
while 1:
    response = requests.get(
        "https://api.iex.cloud/v1/data/core/quote/aapl?token=pk_9458a38e10dd4d40bfe7c9a106550cc9"
    )

    print(response)
    data = {"price":response.json()[0]['iexRealtimePrice'],
            "time": response.json()[0]['latestTime']}

    message_producer = KafkaPro.MessageProducer(broker, topic)

    res = message_producer.send_message(data)
    print(res)
