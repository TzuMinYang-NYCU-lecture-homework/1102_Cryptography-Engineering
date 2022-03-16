import re
import numpy as np

input_str = "ECDTM ECAERAUOOL EDSAM MERNENASSO DYTNR VBNLCRLTIQLAETR IGAWE BAAEIHOR"
input_str = re.sub("[^A-Z]", "", input_str) # 只留A-Z

def compute_difference(row_num, column_num):
    input_arr = np.array(list(input_str)).reshape(column_num, row_num).T    # 因為要轉置，所以reshape的時候col和row要相反
    aver = round(column_num * 0.4, 3)
    diff = 0

    for r in range(row_num):
        vowel_num = 0
        for c in range(column_num):
            if input_arr[r][c] in ('A', 'E', 'I', 'O', 'U'):
                vowel_num = vowel_num + 1
        diff = round(diff + abs(vowel_num - aver), 3)

    print(f'{input_arr}\n{row_num} * {column_num}\'s difference is {diff}\n')

    return diff

if __name__ == "__main__":
    diff7_9 = compute_difference(7, 9) # 7 * 9
    diff9_7 = compute_difference(9, 7) # 9 * 7

    if diff7_9 <= diff9_7:
        print(f'7 * 9 is better.')
    else:
        print(f'9 * 7 is better.')