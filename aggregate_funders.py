import pickle
import json
from os.path import exists
from web3 import Web3

app_name = "Found Wallets Funders"

def aggregateFunders(address):
    funders = {}
    nbr_file_in = 0
    tx_in = 0
    while exists(f"{address}/funding_transactions-{nbr_file_in}.pkl"):
        dataset = pickle.load(open(f"{address}/funding_transactions-{nbr_file_in}.pkl", "rb"))
        nbr_file_in += 1
        for transaction in dataset:
            tx_in += 1
            from_adr = dataset[transaction]["from"]
            if from_adr not in funders:
                funders[from_adr] = {
                    "total_value": int(dataset[transaction]["value"]),
                    "total_gas": int(dataset[transaction]["gas"]),
                    "seen": 1,
                    "funded": [{
                        "wallet": dataset[transaction]["to"],
                        "value": int(dataset[transaction]["value"])
                        }]
                    }
            else:
                funders[from_adr]["total_value"] += int(dataset[transaction]["value"])
                funders[from_adr]["total_gas"] += int(dataset[transaction]["gas"])
                funders[from_adr]["seen"] += 1
                funders[from_adr]["funded"].append({
                        "wallet": dataset[transaction]["to"],
                        "value": int(dataset[transaction]["value"])
                        })
    ordered_funders = dict()
    for from_adr in funders:
        if funders[from_adr]["seen"] > 1:
            ordered_funders[from_adr] = funders[from_adr]
    sorted_keys = sorted((key for key in ordered_funders), key=lambda x: ordered_funders[x]['seen'], reverse=True)
    with open(f"{address}/Result.json", "w") as f:
        f.write('{\n')
        for s in sorted_keys:
            f.write(f"\"{Web3.toChecksumAddress(s)}\": {json.dumps(ordered_funders[s])}")
            if s != sorted_keys[-1]:
                f.write(',\n')
        f.write('}')
    for x in ordered_funders:
        ordered_funders[x].pop('funded')
    with open(f"{address}/Result-short.json", "w") as f:
        f.write('{\n')
        for s in sorted_keys:
            f.write(f"\"{Web3.toChecksumAddress(s)}\": {json.dumps(ordered_funders[s])}")
            if s != sorted_keys[-1]:
                f.write(',\n')
        f.write('}')