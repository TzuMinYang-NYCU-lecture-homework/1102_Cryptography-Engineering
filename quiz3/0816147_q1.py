import re
import numpy as np

def compute_ic(input_str): # from quiz2
    str_len = len(input_str)

    num_letters  = [0] * 26
    for char in input_str:
        num_letters[ord(char) - 65] += 1    # 紀錄A-Z數量

    ic = sum([entry * (entry - 1) for entry in num_letters]) / (str_len * (str_len - 1))

    return ic

def compute_key_len(cypher):
    cypher_len = len(cypher)
    ans_len = 2
    ans_ic = 0
    iter_num = 9 # 助教hint說 3 < key < 8

    for key_len in range(2, iter_num):
        average_ic = 0

        for group in range(key_len):
            cypher_oneline = cypher[np.arange(group, cypher_len, key_len)]
            average_ic += compute_ic(cypher_oneline)
        
        average_ic = average_ic / key_len
        if abs(ans_ic - 0.66) > abs(average_ic - 0.66):  #!!! 不確定要取最大的還是最接近0.66的，這邊是取接近0.66的，或可能最大的只會是最接近0.66的。這邊沒有考慮算到key的倍數時的情況
            ans_len = key_len
            ans_ic = average_ic
    
    return ans_len


if __name__ == "__main__":
    cypher = input()
    cypher = re.sub("[^A-Z]", "", cypher) # 只留A-Z
    cypher = np.array(list(cypher))

    print(f'key len: {compute_key_len(cypher)}')