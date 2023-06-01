from get_transactions import getTransactions
from found_wallets_funders import getFundingTx
from aggregate_funders import aggregateFunders
from web3 import Web3, HTTPProvider
from config import HTTP_PROVIDER, ETHERSCAN_APIKEY
import os

#instantiate a web3 remote provider
w3 = Web3(HTTPProvider(HTTP_PROVIDER))

#etherscan apikey
etherscan_apikey = ETHERSCAN_APIKEY

#request the latest block number
ending_blocknumber = w3.eth.blockNumber #specific or w3.eth.blockNumber

#first requested block number
starting_blocknumber = 17361639 #Pick few blocks after contract creation

#filter through blocks and look for transactions involving this address
address = "0xC3681A720605bD6F8fe9A2FaBff6A7CDEcDc605D"

#filter for specific contract function
contract_function = ""

#side of the tx 0 = from; 1 = to; 2 = both
side = 1

def main():
    if not os.path.exists(address):
        os.makedirs(address)
    getTransactions(w3, starting_blocknumber, ending_blocknumber, address, contract_function, side)
    getFundingTx(etherscan_apikey, address)
    aggregateFunders(address)

if __name__ == '__main__':
    main()