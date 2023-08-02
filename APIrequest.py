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
        "https://api.iex.cloud/v1/data/core/quote/aapl?token=sk_0b416928c4eb474fb320e01f47904d31"
    )
    
    print(response)
    data = response.json()
    
    broker = "localhost:29092"
    topic = "StockPrices"
    
    message_producer = KafkaPro.MessageProducer(broker, topic)
    
    res = message_producer.send_message(data)
    print(res)


