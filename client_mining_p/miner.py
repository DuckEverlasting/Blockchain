import hashlib
import requests
import json

import sys


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:6] == '000000'

def proof_of_work(block):
    block_string = json.dumps(block, sort_keys=True).encode()
    proof = 0
    while valid_proof(block_string, proof) is False:
        proof += 1
    
    return proof


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        response = requests.get(url=f'{node}/last_block')
        last_block = response.json()['last_block']
        proof = proof_of_work(last_block)
        
        response = requests.post(url=f'{node}/mine', json={"proof": proof})

        if response.json()["message"] == 'New Block Forged':
            coins_mined += 1
            print(coins_mined)
        else:
            print(response.json()["message"])
