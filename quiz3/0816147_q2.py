import re
import numpy as np

english_frequency = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.458, 0.978, 2.360, 0.150, 1.974, 0.074]

def compute_ic(input_str):  # from quiz2
    str_len = len(input_str)

    num_letters  = [0] * 26
    for char in input_str:
        num_letters[ord(char) - 65] += 1    # 紀錄A-Z數量

    ic = sum([entry * (entry - 1) for entry in num_letters]) / (str_len * (str_len - 1))

    return ic

def compute_key_len(cypher): # from quiz3 q1
    cypher_len = len(cypher)
    ans_len = 2
    ans_ic = 0
    iter_num = 9 # 助教hint說 3 < key < 8

    for key_len in range(2, iter_num):
        average_ic = 0

        for group in range(key_len):
            cypher_group = cypher[np.arange(group, cypher_len, key_len)]
            average_ic += compute_ic(cypher_group)
        
        average_ic = average_ic / key_len
        if abs(ans_ic - 0.66) > abs(average_ic - 0.66):  #!!! 不確定要取最大的還是最接近0.66的，這邊是取接近0.66的，或可能最大的只會是最接近0.66的。這邊沒有考慮算到key的倍數時的情況
            ans_len = key_len
            ans_ic = average_ic
    
    return ans_len

def compute_key_i(cypher_group):
    str_len = len(cypher_group)
    cypher_frequency = [0] * 26
    for char in cypher_group:
        cypher_frequency[ord(char) - 65] += 1
    
    cypher_frequency = [cypher_frequency[i] / str_len for i in range(26)]

    ans_shift = 0
    ans_value = 0
    for shift in range(25):
        value = sum([cypher_frequency[(i + shift) % 26] * english_frequency[i] for i in range(26)])
        
        if value > ans_value:
            ans_shift, ans_value = shift, value

    return chr(ans_shift + 65)


def compute_key(key_len, cypher):
    cypher_len = len(cypher)
    key = ""
    for group in range(key_len):
        cypher_group = cypher[np.arange(group, cypher_len, key_len)]
        key += compute_key_i(cypher_group)

    return key

def decrypt(key, cypher):
    key_len = len(key)
    plaintext = ""
    for i in range(len(cypher)):
        plaintext += chr(((ord(cypher[i]) - ord(key[i % key_len])) % 26) + 65)  # %的結果會自己取成正的
    
    return plaintext

if __name__ == "__main__":
    english_frequency = [english_frequency[i] / 100 for i in range(26)]

    cypher = input()
    cypher = re.sub("[^A-Z]", "", cypher) # 只留A-Z
    cypher = np.array(list(cypher))

    key_len = compute_key_len(cypher)
    key = compute_key(key_len, cypher)
    #plaintext = decrypt(key, cypher)

    #print(f'key len: {key_len}\nkey: {key}\nplaintext: {plaintext}')
    print(key)