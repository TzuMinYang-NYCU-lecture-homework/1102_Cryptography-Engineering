#!/bin/python

import string
import math
import random

def create_cipher_dict(key):
    cipher_dict = {}
    alphabet_list = list(string.ascii_uppercase)
    for i in range(len(key)):
        cipher_dict[alphabet_list[i]] = key[i]

    return cipher_dict

def encrypt(text, key):
    cipher_dict = create_cipher_dict(key)
    text = list(text)
    newtext = ""
    for elem in text:
        if elem.upper() in cipher_dict:
            newtext += cipher_dict[elem.upper()]
        else:
            newtext += " "
    return newtext

# This function takes input as a path to a long text and creates scoring_params dict which contains the
# number of time each pair of alphabet appears together
# Ex. {'AB':234,'TH':2343,'CD':23 ..}
# Note: Take whitespace into consideration

def create_scoring_params_dict(longtext_path):
    #TODO
    pass

# This function takes input as a text and creates scoring_params dict which contains the
# number of time each pair of alphabet appears together
# Ex. {'AB':234,'TH':2343,'CD':23 ..}
# Note: Take whitespace into consideration

def score_params_on_cipher(text):
    #TODO
    pass

# This function takes the text to be decrypted and a cipher to score the cipher.
# This function returns the log(score) metric

def get_cipher_score(text,cipher,scoring_params):
    #TODO
    pass


# Generate a proposal cipher by swapping letters at two random location
def generate_cipher(cipher):
    #TODO
    pass

# Toss a random coin with robability of head p. If coin comes head return true else false.
def random_coin(p):
    #TODO
    pass

# Takes input as a text to decrypt and runs a MCMC algorithm for n_iter. Returns the state having maximum score and also
# the last few states
def MCMC_decrypt(n_iter,cipher_text,scoring_params):
    current_cipher = string.ascii_uppercase # Generate a random cipher to start
    best_state = ''
    score = 0
    for i in range(n_iter):
        proposed_cipher = generate_cipher(current_cipher)
        score_current_cipher = get_cipher_score(cipher_text,current_cipher,scoring_params)
        score_proposed_cipher = get_cipher_score(cipher_text,proposed_cipher,scoring_params)
        acceptance_probability = min(1,math.exp(score_proposed_cipher-score_current_cipher))
        if score_current_cipher>score:
            best_state = current_cipher
        if random_coin(acceptance_probability):
            current_cipher = proposed_cipher
        if i%500==0:
            print("iter",i,":",encrypt(cipher_text,current_cipher)[0:99])
    return best_state

def main():
    ## Run the Main Program:

    scoring_params = create_scoring_params_dict('war_and_peace.txt')

    with open('ciphertext.txt','r') as f:
        cipher_text = f.read()
    print(cipher_text)

    print("Text To Decode:", cipher_text)
    print("\n")
    best_state = MCMC_decrypt(10000,cipher_text,scoring_params)
    print("\n")
    plain_text = encrypt(cipher_text,best_state)
    print("Decoded Text:",plain_text)
    print("\n")
    print("MCMC KEY FOUND:",best_state)

    with open('plaintext.txt','w+') as f:
        f.write(plain_text)


if __name__ == '__main__':
    main()
