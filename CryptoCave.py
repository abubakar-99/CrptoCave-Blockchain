
import time
from mnemonic import Mnemonic
from termcolor import colored
from web3 import Web3
from eth_account import Account
import requests

print(colored("""
 ▄████▄   ██▀███ ▓██   ██▓ ██▓███  ▄▄▄█████▓ ▒█████      ▄████▄   ▄▄▄    ██▒   █▓▓█████    
▒██▀ ▀█  ▓██ ▒ ██▒▒██  ██▒▓██░  ██▒▓  ██▒ ▓▒▒██▒  ██▒   ▒██▀ ▀█  ▒████▄ ▓██░   █▒▓█   ▀    
▒▓█    ▄ ▓██ ░▄█ ▒ ▒██ ██░▓██░ ██▓▒▒ ▓██░ ▒░▒██░  ██▒   ▒▓█    ▄ ▒██  ▀█▄▓██  █▒░▒███      
▒▓▓▄ ▄██▒▒██▀▀█▄   ░ ▐██▓░▒██▄█▓▒ ▒░ ▓██▓ ░ ▒██   ██░   ▒▓▓▄ ▄██▒░██▄▄▄▄██▒██ █░░▒▓█  ▄    
▒ ▓███▀ ░░██▓ ▒██▒ ░ ██▒▓░▒██▒ ░  ░  ▒██▒ ░ ░ ████▓▒░   ▒ ▓███▀ ░ ▓█   ▓██▒▒▀█░  ░▒████▒   
░ ░▒ ▒  ░░ ▒▓ ░▒▓░  ██▒▒▒ ▒▓▒░ ░  ░  ▒ ░░   ░ ▒░▒░▒░    ░ ░▒ ▒  ░ ▒▒   ▓▒█░░ ▐░  ░░ ▒░ ░   
  ░  ▒     ░▒ ░ ▒░▓██ ░▒░ ░▒ ░         ░      ░ ▒ ▒░      ░  ▒     ▒   ▒▒ ░░ ░░   ░ ░  ░   
░          ░░   ░ ▒ ▒ ░░  ░░         ░      ░ ░ ░ ▒     ░          ░   ▒     ░░     ░      
░ ░         ░     ░ ░                           ░ ░     ░ ░            ░  ░   ░     ░  ░   
░                 ░ ░                                   ░                    ░             
""","cyan"))

key = "key|UAvtJEYkQnT47JBDfCpDmpq2Rx5z7VAF"
premium = input("Enter license key: ")

if key == premium:
    print(colored("Connecting to server....", "green"))
    time.sleep(10)
    print(colored("Successfully connected!", "green"))
else:
    print(colored("Invalid license key! Exiting program.", "red"))
    exit()

# Enable HD Wallet features
Account.enable_unaudited_hdwallet_features()

# Alchemy API key
ALCHEMY_API_KEY = "i--jiFMmALiKL10pi56-kuUekS3gSWBM"  # Your Alchemy API key

# Alchemy Nodes for supported blockchains
ALCHEMY_NODES = {
    "Ethereum": f"https://eth-mainnet.alchemyapi.io/v2/{ALCHEMY_API_KEY}",
    "Polygon": f"https://polygon-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}",
    "BTC": f"https://arb1.arbitrum.io/rpc",  # Using Alchemy for BTC (Arbitrum)
    "Solana": f"https://solana-mainnet.rpc.alchemy.com/v1/{ALCHEMY_API_KEY}",  # Solana support with Alchemy
    "BSC": f"https://bsc-dataseed.binance.org/",  # Binance Smart Chain RPC
}

# TRON Node URL
TRON_NODE = "https://api.trongrid.io"

# Web3 connections for supported blockchains using Alchemy
WEB3_CONNECTIONS = {name: Web3(Web3.HTTPProvider(url)) for name, url in ALCHEMY_NODES.items()}

# Supported blockchains
SUPPORTED_CHAINS = list(WEB3_CONNECTIONS.keys()) + ["TRON"]  # Added TRON and removed BTC (since BTC is just renamed Arbitrum)

# CoinGecko API URL for getting current prices
COINGECKO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

# Function to get the price of a cryptocurrency in USD using CoinGecko
def get_price_in_usd(crypto_symbol):
    try:
        response = requests.get(f"{COINGECKO_API_URL}?ids={crypto_symbol}&vs_currencies=usd")
        response.raise_for_status()
        data = response.json()
        return data[crypto_symbol]["usd"]
    except:
        return 0

# Check ETH-based balance using Web3
def check_balance_web3(address, blockchain_name, w3_connection):
    try:
        balance = w3_connection.eth.get_balance(address)
        return balance / 10**18  # Convert wei to ether or equivalent token (BSC uses BNB as well)
    except:
        return 0

# Check TRON balance using TRON API
def check_balance_tron(address):
    try:
        url = f"{TRON_NODE}/v1/accounts/{address}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        balance = data.get("data", [{}])[0].get("balance", 0)
        return balance / 1_000_000  # Convert sun to trx (1 trx = 1,000,000 sun)
    except:
        return 0

# Check BNB balance using Web3 (BSC)
def check_balance_bnb(address, blockchain_name, w3_connection):
    try:
        balance = w3_connection.eth.get_balance(address)
        return balance / 10**18  # Convert wei to BNB
    except:
        return 0

# Generate a random mnemonic phrase
def generate_random_mnemonic(num_words=12):
    mnemo = Mnemonic("english")
    return mnemo.generate(strength=128 if num_words == 12 else 256)

# Generate an Ethereum address from the mnemonic
def generate_eth_address(mnemonic):
    try:
        account = Account.from_mnemonic(mnemonic)
        return account.address
    except:
        return None

# Check wallet balance for all supported blockchains
def check_wallet_balance(mnemonic, selected_blockchain=None):
    address = generate_eth_address(mnemonic)
    if not address:
        return []

    # Display the mnemonic and address here
    print(colored(f"\nMnemonic: {mnemonic}", "cyan"))
    with open("results.txt", "a") as f:
        f.write(f"Mnemonic: {mnemonic}\n")

    results = []

    # Check balance for all supported blockchains
    for blockchain_name, w3_connection in WEB3_CONNECTIONS.items():
        if selected_blockchain and blockchain_name != selected_blockchain:
            continue

        if blockchain_name == "BSC":
            balance = check_balance_bnb(address, blockchain_name, w3_connection)
            symbol = "bnb"
        else:
            balance = check_balance_web3(address, blockchain_name, w3_connection)
            symbol = blockchain_name.lower()

        # Get price in USD
        price_in_usd = get_price_in_usd(symbol)
        balance_in_usd = balance * price_in_usd if price_in_usd > 0 else 0
        
        results.append((blockchain_name, address, balance, balance_in_usd))

        # Always print the balance, even if it's zero
        if balance > 0:
            print(f"{blockchain_name} Balance: {balance:.4f} | USD: ${balance_in_usd:.2f}")
        else:
            print(f"{blockchain_name} Balance: 0.0000 | USD: $0.00")

    # Check TRON balance
    if selected_blockchain in ["TRON", None]:
        trx_balance = check_balance_tron(address)
        price_in_usd = get_price_in_usd("tron")
        trx_balance_in_usd = trx_balance * price_in_usd if price_in_usd > 0 else 0
        
        results.append(("TRON", address, trx_balance, trx_balance_in_usd))

        # Always print the TRON balance, even if it's zero
        if trx_balance > 0:
            print(f"TRON Balance: {trx_balance:.4f} | USD: ${trx_balance_in_usd:.2f}")
        else:
            print(f"TRON Balance: 0.0000 | USD: $0.00")

    return results
# Main function
def main():
    print(colored("""
    _______________________________________________________
    |                                                      |
    | _______________________        ▄▄█▀▀▀▀▀█▄▄           |
    | |                     |      ▄█▀░░▄░▄░░░░▀█▄         |
    | |  MENU OPTION        |      █░░░▀█▀▀▀▀▄░░░█         |
    | |_____________________|      █░░░░█▄▄▄▄▀░░░█         |
    |                              █░░░░█░░░░█░░░█         |
    | 1. Blockchain list            ▀█▄░▀▀█▀█▀░░▄█         |
    | 2. Multi-Coin                   ▀▀█▄▄▄▄▄█▀▀          |
    | 3. t.me/Namberdar_Devolper      Crypto cave          |           
    |______________________________________________________|
    |                                                     | 
    |  Enter your choice:                                 |
    |_____________________________________________________| 
    """, "cyan"))

    option = input("Select option (1 or 2): ")
    if option == "1":
        print("\nSupported Blockchains:")
        for idx, blockchain in enumerate(SUPPORTED_CHAINS, start=1):
            print(f"{idx}. {blockchain}")

        blockchain_choice = int(input("Select blockchain by number: "))
        selected_blockchain = SUPPORTED_CHAINS[blockchain_choice - 1]
        print(colored(f"Selected Blockchain: {selected_blockchain}", "cyan"))
    elif option == "2":
        selected_blockchain = None
        print(colored("Multi-Coin mode selected. Checking all blockchains.", "cyan"))
    else:
        print(colored("Invalid option. Please restart the program.", "red"))
        return

    total_checked = 0
    total_found = 0

    while True:
        # Generate mnemonic and check balances
        mnemonic = generate_random_mnemonic()
        total_checked += 1

        results = check_wallet_balance(mnemonic, selected_blockchain)
        
        # Check if at least one non-zero balance is found
        if any(balance > 0 for _, _, balance, _ in results):
            total_found += 1
            print(colored("\nNon-zero wallet(s) found!", "cyan"))
            for blockchain_name, address, balance, balance_in_usd in results:
                print(f"Blockchain: {blockchain_name}")
                print(f"Address: {address}")
                print(f"Balance: {balance:.4f}")
                print(f"Balance in USD: ${balance_in_usd:.2f}")
            break
        else:
            print(colored("\nNo non-zero wallet found. Trying another...", "cyan"))
            print(colored(f"Total wallets checked: {total_checked}", "cyan"))
            print(colored(f"Total non-zero wallets found: {total_found}", "cyan"))

# Start the program
if __name__ == "__main__":
    main()


