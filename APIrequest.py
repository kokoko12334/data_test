import requests
import KafkaPro


# base_url = "https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey="
# key_url = base_url + "z48%2F32jB2tRjAxudA7CAxOsf8K1us6N3OWL140lPkCe4FCnB1Tfpggkw7dV6OTGzRxCJ07x4xnodJ2HCIqaowA%3D%3D"

# final_url = key_url+(
#                     "&resultType=json"
#                     "&numOfRows=250"
#                     "&beginBasDt=20210906"
#                     "&endBasDt=20220906"
#                     "&likeSrtnCd=005930"
#                     )


for _ in range(10000):
    response = requests.get(
        "https://api.iex.cloud/v1/data/core/quote/aapl?token=pk_9458a38e10dd4d40bfe7c9a106550cc9"
    )
    
    print(response)
    data = response.json()
    
    broker = "localhost:29092"
    topic = "StockPrices"
    
    message_producer = KafkaPro.MessageProducer(broker, topic)
    
    res = message_producer.send_message(data)
    print(res)


