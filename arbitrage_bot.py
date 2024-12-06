import requests
import ccxt
import random  # For simulating random price fluctuations
import keyboard  # Add this import at the top of your file
import time  # Add this import at the top of your file

# Initialize exchanges with fake balances
balances = {
    'Binance': 1000,  # Fake money in USD
    'Kraken': 1000,
    'Huobi': 1000,
    'Bitfinex': 1000,
    'Coinbase Pro': 1000,
}

# Initialize exchanges
binance = ccxt.binance()
kraken = ccxt.kraken()
huobi = ccxt.huobi()
bitfinex = ccxt.bitfinex()
coinbase = ccxt.coinbase()
mexc = ccxt.mexc()
bingx = ccxt.bingx()
gate = ccxt.gate()
bybit = ccxt.bybit()


# List of cryptocurrencies to check
cryptos = ['SOL/USDT']  # Add more pairs as needed

def find_best_arbitrage_opportunity():
    best_opportunity = None
    best_profit_percentage = 0
    tickers = {}

    for crypto in cryptos:
        print("fetching " + crypto)
        tickers = {
            'Binance': binance.fetch_ticker(crypto)['last'],
            'Kraken': kraken.fetch_ticker(crypto)['last'],
            'Huobi': huobi.fetch_ticker(crypto)['last'],
            'Bitfinex': bitfinex.fetch_ticker(crypto)['last'],
            'Coinbase Pro': coinbase.fetch_ticker(crypto)['last'],
        }

        for exchange_a, price_a in tickers.items():
            for exchange_b, price_b in tickers.items():
                if exchange_a != exchange_b:
                    if price_a < price_b:
                        profit = price_b - price_a
                        profit_percentage = (profit / price_a) * 100
                        if profit_percentage > best_profit_percentage:
                            best_profit_percentage = profit_percentage
                            best_opportunity = (crypto, exchange_a, exchange_b, profit_percentage)
                            # Check if there are sufficient funds before simulating the trade
                            if balances[exchange_a] >= price_a:
                                simulate_trade(exchange_a, exchange_b, crypto, 20, tickers)
                    elif price_b < price_a:
                        profit = price_a - price_b
                        profit_percentage = (profit / price_b) * 100
                        if profit_percentage > best_profit_percentage:
                            best_profit_percentage = profit_percentage
                            best_opportunity = (crypto, exchange_b, exchange_a, profit_percentage)
                            # Check if there are sufficient funds before simulating the trade
                            if balances[exchange_b] >= price_b:
                                simulate_trade(exchange_b, exchange_a, crypto, 20, tickers)

    return best_opportunity, tickers  # Return both the opportunity and tickers

def simulate_trade(buy_exchange, sell_exchange, crypto, euro_amount, tickers):
    buy_price = tickers[buy_exchange]
    sell_price = tickers[sell_exchange]
    
    # Calculate the amount of SOL to buy for the given euro amount
    amount = euro_amount / buy_price
    
    cost = buy_price * amount
    profit = (sell_price - buy_price) * amount
    
    # Fixed transaction fee
    transaction_fee = 0.015  # $0.015 fee
    
    # Adjust profit for transaction fee
    profit -= transaction_fee
    
    if balances[buy_exchange] < cost:
        print(f"Insufficient funds on {buy_exchange} to buy {amount:.4f} of {crypto}. Trade not executed.")
        return
    
    # Update balances
    balances[buy_exchange] -= cost  # Deduct only the cost
    balances[sell_exchange] += (cost + profit)  # Add the entire amount (cost + profit) to the selling exchange
    
    print(f"Simulated trade: Buy {amount:.4f} of {crypto} on {buy_exchange} at {buy_price}, "
          f"Sell on {sell_exchange} at {sell_price}, Profit after fees: {profit:.2f}")
    
    print("Updated Balances:")
    for exchange, balance in balances.items():
        print(f"{exchange}: {balance:.2f}")
    
    # Print total balance across all exchanges
    total_balance = sum(balances.values())
    print(f"Total Balance: {total_balance:.2f}\n")  # Print total balance after each trade

# Main loop to keep running until 'q' is pressed
while True:
    best_opportunity, tickers = find_best_arbitrage_opportunity()  # Get both values
    if best_opportunity:
        crypto, buy_exchange, sell_exchange, profit_percentage = best_opportunity
        print(f"Best Arbitrage Opportunity: Buy {crypto} on {buy_exchange} and sell on {sell_exchange} for a profit of {profit_percentage:.2f}%")
        
        # Check if there are sufficient funds to execute the trade
        if balances[buy_exchange] >= tickers[buy_exchange]:  # Ensure sufficient funds
            simulate_trade(buy_exchange, sell_exchange, crypto, 20, tickers)  # Simulate trading €20
        else:
            print(f"Insufficient funds on {buy_exchange} to execute trade.")
    else:
        print("No arbitrage opportunity found.")
    
    # Check for user input to exit
    if keyboard.is_pressed('q'):
        print("Exiting the arbitrage bot.")
        break
    
    time.sleep(1)  # Add a delay to allow for market changes
