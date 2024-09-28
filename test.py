import requests

token = "6501489744:AAEVS3aoQG1JsbkJBWRdTWw7__JuWJvF43w"

chat_id = 1234746517

url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=тест"
requests.get(url)