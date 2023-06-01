import pickle
import requests
import json
import time
from os.path import exists

nbr_block_before = 652072 #7240 per day

def check_internal_txs(address, blockNumber, apikey):
    req = f"https://api.etherscan.io/api?module=account&action=txlistinternal&address={address}&startblock={blockNumber-nbr_block_before}&endblock={blockNumber}&page=1&offset=100&sort=desc&apikey={apikey}"
    try:
        response = requests.get(req, timeout=30)
    except Exception as e:
        print(e)
        time.sleep(10)
        return {}
    if response.status_code != 200:
        print(f"{response.status_code}: {req}")
        time.sleep(1)
    transactions = json.loads(response.text)
    if transactions['result'] == []:
        print(f"None found for {address}")
        return {}
    for transaction in transactions['result']:
        if transaction['to'].lower() == address.lower() and int(transaction['value']) > 0:
            return transaction
    time.sleep(0.2)
    return {}

def check_last_wallet_funder(address, blockNumber, apikey):
    for page in range(1, 10):
        req = f"https://api.etherscan.io/api?module=account&action=txlist&address={address}&startblock={blockNumber-nbr_block_before}&endblock={blockNumber}&page={page}&offset=100&sort=desc&apikey={apikey}"
        try:
            response = requests.get(req, timeout=30)
            time.sleep(0.2)
        except Exception as e:
            print(e)
            print("Sleep 10 secondes and retry")
            time.sleep(10)
            continue
        if response.status_code != 200:
            print(f"{response.status_code}: {req}")
            time.sleep(1)
        try:
            transactions = json.loads(response.text)
        except Exception as e:
            print(e)
            continue
        if transactions['result'] == []:
            return check_internal_txs(address, blockNumber, apikey)
        for transaction in transactions['result']:
            if transaction['to'].lower() == address.lower() and int(transaction['value']) > 0:
                return transaction
    return {}

def getFundingTx(apikey, address):
    '''The function loops over the transactions founds in the previous step, grab the address who initiated the tx and
    checks for the wallet who fund it. Check in internal transactions if needed.'''
    tx_dictionary = {}
    nbr_file_in = 0
    nbr_file_out = 0
    tx_in = 0
    tx_spotted = 0
    while exists(f"{address}/transactions-{nbr_file_in}.pkl"):
        dataset = pickle.load(open(f"{address}/transactions-{nbr_file_in}.pkl", "rb"))
        nbr_file_in += 1
        for transaction in dataset:
            tx_in += 1
            # print (data[transaction]['from'])
            fund_tx = check_last_wallet_funder(dataset[transaction]['from'], dataset[transaction]['blockNumber'], apikey)
            if fund_tx != {}:
                tx_spotted += 1
                with open(f"{address}/funding_transactions-{nbr_file_out}.pkl", "wb") as f:
                    hashStr = fund_tx['hash']
                    tx_dictionary[hashStr] = fund_tx
                    pickle.dump(tx_dictionary, f)
                if tx_spotted % 10000 == 0:
                    nbr_file_out += 1
                    tx_dictionary = {}
                if tx_spotted == 1:
                    print(f"Found the first funding tx : {fund_tx}")
        print(f"End on input file n°{nbr_file_in} output file n°{nbr_file_out}")
        print(f"Spotted {tx_spotted} funding tx so far on {tx_in} address ({tx_spotted / tx_in * 100}%)")