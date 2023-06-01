import pickle
from web3 import Web3

def getTransactions(w3, start, end, address, function = "", side = 2):
    '''The function loops over the transactions in each block and
    checks if the address in the to field matches the one we set in the contract_address.
    Additionally, it will write the found transactions to a pickle file for quickly serializing and de-serializing
    a Python object.'''
    address = Web3.toChecksumAddress(address)
    nbr_file = 0
    tx_spotted = 0
    tx_dictionary = {}
    print(f"Started filtering through block number {start} to {end} for transactions involving the address - {address}")
    diff_block = end - start
    old_percents = 100
    for blocknumber in range(start, end + 1):
        block = w3.eth.get_block(blocknumber, True)
        percents = round(100.0 * (blocknumber - start) / float(diff_block), 1)
        if percents != old_percents:
            old_percents = percents
            if percents % 5 == 0:
                print (f"Block {blocknumber} - {percents}% completed")
        for transaction in block.transactions:
            try:
                if (side in [0, 2] and transaction['from'] == address) or (side in [1, 2] and transaction['to'] == address):
                    tx_spotted += 1
                    with open(f"{address}/transactions-{nbr_file}.pkl", "wb") as f:
                        hashStr = transaction['hash'].hex()
                        tx_dictionary[hashStr] = transaction
                        if function == "" or transaction['input'][0:10] == function:
                            pickle.dump(tx_dictionary, f)
                    if tx_spotted % 10000 == 0:
                        nbr_file += 1
                        tx_dictionary = {}
                        print(f"Spotted {tx_spotted} tx so far")
                    if tx_spotted == 1:
                        print(f"Found the first interaction : {transaction}")
            except Exception as e:
                print (e)
    print(f"Finished searching blocks {start} through {end} and found {tx_spotted} transactions")
    