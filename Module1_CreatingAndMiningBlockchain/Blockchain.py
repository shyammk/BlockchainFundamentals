# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 21:58:57 2018

@author: shyam_mk
"""

# Import the required libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

# Building a block-chain
class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.createBlock(proof = 1, prevHash = '0')
    
    # Function to create a new block
    def createBlock(self, proof, prevHash):
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'prevHash': prevHash}
        self.chain.append(block)
        return block
    
    # Function to get the previous (last) block in the chain
    def getPreviousBlock(self):
        return self.chain[-1]
    
    # Function to find the golden nonce or proof of work
    def getProofOfWork(self, prevProof):
        newProof = 1
        proofFlag = False
        while proofFlag is False:
            hashValue = hashlib.sha256(str(newProof**2 - prevProof**2).encode()).hexdigest()
            if hashValue[:4] == '0000':
                proofFlag = True
            else:
                newProof += 1
        return newProof
    
    # Function to hash a block
    def findHash(self, block):
        encodedBlock = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encodedBlock).hexdigest()
    
    # Function to verify if the blockchain is valid or not
    def checkChainValidity(self, chain):
        prevBlock = chain[0]
        blockIndex = 1
        while blockIndex < len(chain):
            curBlock = chain[blockIndex]
            if(curBlock['prevHash'] != self.findHash(prevBlock)):
                return False
            prevProof = prevBlock['proof']
            curProof = curBlock['proof']
            hashValue = hashlib.sha256(str(curProof**2 - prevProof**2).encode()).hexdigest()
            if hashValue[:4] != '0000':
                return False
            prevBlock = curBlock
            blockIndex += 1
        return True
    
# Mining the block-chain

# Creating the flask web app
flaskWebApp = Flask(__name__)

# Create an instance of blockchain
blockChain = Blockchain()

# Mining a new block
@flaskWebApp.route('/mine_block', methods = ['GET'])
def mineBlock():
    previousBlock = blockChain.getPreviousBlock()
    previousProof = previousBlock['proof']
    newProof = blockChain.getProofOfWork(previousProof)
    previousHashValue = blockChain.findHash(previousBlock)
    newBlock = blockChain.createBlock(newProof, previousHashValue)
    response = {'message': 'Congratz. You just mined a block!',
                'index': newBlock['index'],
                'timestamp': newBlock['timestamp'],
                'proof': newBlock['proof'],
                'prevHash': newBlock['prevHash']}
    return jsonify(response), 200

# Fetching the full blockchain
@flaskWebApp.route('/get_chain', methods = ['GET'])
def getChain():
    response = {'chain': blockChain.chain,
                'chainLength': len(blockChain.chain)}
    return jsonify(response), 200    

# Check if the blockchain is valid
@flaskWebApp.route('/is_valid', methods = ['GET'])
def isChainValid():
    validityFlag = blockChain.checkChainValidity(blockChain.chain)
    if validityFlag:
        response = {'message': 'Wow. The blockchain is valid!'}
    else:
        response = {'message': 'Oops. The blockchain is invalid!'}
    return jsonify(response), 200

# Executing the web app
flaskWebApp.run(host = '0.0.0.0', port = 5000)
        
        
        
        