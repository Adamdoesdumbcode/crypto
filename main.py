import requests
import os

API_KEY = "xxxxx" # Put your API key for CoinMarketCap HERE
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/info'

headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': API_KEY,
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def search_coin(identifier):
    params = {'symbol': identifier.upper()} if not identifier.startswith("0x") else {'address': identifier}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get('data', {})
    else:
        return {'error': response.json().get('status', {}).get('error_message', 'Unknown error')}

def start():
    while True:
        clear_screen()
        query = input("Enter token name, Symbol, or contract address (or type 'exit' to quit): ").strip()

        if query.lower() == 'exit':
            print("Exiting the program...")
            break

        result = search_coin(query)

        if 'error' in result:
            print(f"Error: {result['error']}")
        else:
            for _, coin in result.items():
                print(f"Name: {coin['name']} ({coin['symbol']})")
                
                # Safely access the 'platform' and 'token_address' fields
                platform = coin.get('platform')
                token_address = platform.get('token_address', 'N/A') if platform else 'N/A'
                print(f"Token Address: {token_address}")

                print(f"Website: {coin.get('urls', {}).get('website', ['N/A'])[0]}")
                print(f"Description: {coin.get('description', 'N/A')}")

                # Display additional info
                if 'quote' in coin:
                    for currency, quote in coin['quote'].items():
                        print(f"Price ({currency}): {quote.get('price', 'N/A')}")
                        print(f"Market Cap ({currency}): {quote.get('market_cap', 'N/A')}")
                        print(f"Circulating Supply ({currency}): {quote.get('circulating_supply', 'N/A')}")

        input("Press Enter to search again or 'exit' to quit...")

# Start the program
start()
