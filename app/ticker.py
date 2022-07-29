import requests
class ticker:
    def get_bitcoin_price():
        r = requests.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false")
        bitcoin_data = None
        for coin in r.json():
            if coin["id"] == "bitcoin":
                bitcoin_data = coin
        return bitcoin_data["current_price"]

    def check_alert(alert):
        if alert.targetPrice == get_bitcoin_price():
            send_email()

if __name__ == "__main__":
    print(type(get_bitcoin_price()))
        
