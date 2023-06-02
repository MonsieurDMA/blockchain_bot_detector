# Blockchain Bot Detector
This script trace wallets interacting with an ethereum address (wallet or smart-contract) and generate data to detect possible bot. The way it work is by finding from where theses wallets got their funds and tag potential owner.

It work with any HTTP RPC (ex: infura) and etherscan api.

The script is splitted in 3 parts that the file [main.py](https://github.com/MonsieurDMA/blockchain_bot_detector/blob/main/main.py) will call.

# Config

You should setup **HTTP_PROVIDER** and **ETHERSCAN_APIKEY**  from [**config.py**](https://github.com/MonsieurDMA/blockchain_bot_detector/blob/main/config.py) with your HTTP RPC and etherscan api key.

In [main.py](https://github.com/MonsieurDMA/blockchain_bot_detector/blob/main/main.py) you can setup the **address** you want to scan, if you want to filter any specific function, the side of the transactions and the range of block you want to analyse.


## Requirements

    pip3 install pickle web3

## Usage

    python3 main.py

A new folder, named by the address you are scanning, will be generated. 

## Generated data
Data are generated in two json file ready to be interpreted, as normal and short version. Examples below.
![enter image description here](https://github.com/MonsieurDMA/blockchain_bot_detector/blob/main/public/sample_result_long.png?raw=true)![enter image description here](https://github.com/MonsieurDMA/blockchain_bot_detector/blob/main/public/sample_result_short.png?raw=true)
## Troubleshooting
If you got any error, please open an issue with as many details as possible.
