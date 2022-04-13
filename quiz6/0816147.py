#!/bin/python

import string
import math
import numpy as np ### add by myslef, for np.exp
import random

def create_cipher_dict(key): ### create a dict which plaintext map to cyphertext 
    cipher_dict = {}
    alphabet_list = list(string.ascii_uppercase)
    for i in range(len(key)):
        cipher_dict[alphabet_list[i]] = key[i]

    return cipher_dict

def encrypt(text, key): ### encrypt text through key, I think it is 'decrypt' not 'encrypt'
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

def create_scoring_params_dict(longtext_path): ### create dict through a pathname
    #TODO
    with open(longtext_path,'r') as f:
        longtext = f.read()

    longtext = longtext.upper()
    score_params_dict = {}
    
    for i in range(len(longtext) - 1):
        if not (longtext[i] in string.ascii_uppercase and longtext[i + 1] in string.ascii_uppercase): 
        ### don't know what problem with'isalpha()' function, it will let "'", "\r", ... etc pass and appear in dict
            continue
        if (longtext[i] + longtext[i + 1]) not in score_params_dict:
            score_params_dict[longtext[i] + longtext[i + 1]] = 1
        else:
            score_params_dict[longtext[i] + longtext[i + 1]] += 1

    #print(score_params_dict)

    return score_params_dict

# This function takes input as a text and creates scoring_params dict which contains the
# number of time each pair of alphabet appears together
# Ex. {'AB':234,'TH':2343,'CD':23 ..}
# Note: Take whitespace into consideration

def score_params_on_cipher(text):  ### create a dict through a string
    #TODO

    text = text.upper()
    score_params_dict = {}
    
    for i in range(len(text) - 1):
        if not (text[i] in string.ascii_uppercase and text[i + 1] in string.ascii_uppercase):
            continue
        if (text[i] + text[i + 1]) not in score_params_dict:
            score_params_dict[text[i] + text[i + 1]] = 1
        else:
            score_params_dict[text[i] + text[i + 1]] += 1

    #print(score_params_dict)

    return score_params_dict

# This function takes the text to be decrypted and a cipher to score the cipher.
# This function returns the log(score) metric

def get_cipher_score(text,cipher,scoring_params):
    #TODO
    plaintext = encrypt(text, cipher)
    cipher_score_params = score_params_on_cipher(plaintext)
    score = 0

    for pair in scoring_params:
        if pair not in cipher_score_params: ### anything not appear is not important
            continue
        score += math.log(scoring_params[pair] * cipher_score_params[pair]) ### turn '*' into '+' and turn 'power' into '*' through log

    return score

# Generate a proposal cipher by swapping letters at two random location
def generate_cipher(cipher):
    #TODO
    change_index = random.sample(range(0, 26), 2) ### range is [a, b), choose 2 numbers which are not the same
    new_cipher = list(cipher) ### string can't change, so I turn it into list
    new_cipher[change_index[0]], new_cipher[change_index[1]] = new_cipher[change_index[1]], new_cipher[change_index[0]]

    return ''.join(new_cipher)

# Toss a random coin with probability of head p. If coin comes head return true else false.
def random_coin(p):
    #TODO
    if random.uniform(0, 1) < p:
        return True
    return False

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

        ### I had meant to replace 'math.exp' by 'np.exp', because 'math.exp' may lead to overflow.
        ### but there is an error in my enviroment, I don't know whether numpy work well in TA's enviroment, so I use try-except statement
        try: 
            acceptance_probability = min(1,math.exp(score_proposed_cipher-score_current_cipher))
        except OverflowError:
            acceptance_probability = 1
            
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
