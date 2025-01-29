# Crypto Wallet Balance Checker


A Python-based crypto wallet balance checker that supports multiple blockchains, including Ethereum, Polygon, Binance Smart Chain (BSC), Tron, and Solana. It uses **Web3.py**, **Alchemy API**, and **CoinGecko API** to fetch wallet balances and their equivalent USD value.

## Features

- 🔑 **Mnemonic-based Wallet Address Generation**
- 🌐 **Supports multiple blockchains** (Ethereum, Polygon, BSC, Tron, Solana)
- 💰 **Fetches real-time balance & USD conversion** using CoinGecko API
- 🔄 **Checks multiple wallets continuously until a non-zero balance is found**
- 🔍 **Validates license key before execution**

## Supported Blockchains
- **Ethereum (ETH)**
- **Polygon (MATIC)**
- **Binance Smart Chain (BNB)**
- **Tron (TRX)**
- **Solana (SOL)**

## Installation

### Prerequisites
Ensure you have Python 3.8+ installed. Install dependencies using:

```sh
pip install -r requirements.txt
```

### Dependencies
- `web3`
- `mnemonic`
- `requests`
- `termcolor`

## Usage

Run the script:

```sh
python main.py
```

You will be prompted to enter a **license key** to proceed.

### Menu Options
1. **Blockchain List** - Manually select a blockchain to check wallet balances.
2. **Multi-Coin Mode** - Checks balances across all supported blockchains.

## API Configuration
- Replace `ALCHEMY_API_KEY` with your **Alchemy API Key**
- Uses **CoinGecko API** to fetch live crypto prices

## License
This project is licensed under the MIT License.

## Disclaimer
This tool is for educational purposes only. Use it responsibly!

## Author
 **Abu Bakar**
