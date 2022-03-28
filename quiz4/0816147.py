import re
import numpy as np
import math

training_text = """
WITHM ALICE TOWAR DNONE WITHC HARIT YFORA LLWIT
HFIRM NESSI NTHER IGHTA SGODG IVESU STOSE ETHER
IGHTL ETUSS TRIVE ONTOF INISH THEWO RKWEA REINT
OBIND UPTHE NATIO NSWOU NDSTO CAREF ORHIM WHOSH
ALLHA VEBOR NETHE BATTL EANDF ORHIS WIDOW ANDHI
SORPH ANTOD OALLW HICHM AYACH IEVEA NDCHE RISHA
JUSTA NDLAS TINGP EACEA MONGO URSEL VESAN DWITH
ALLNA TIONS GREEC EANNO UNCED YESTE RDAYT HEAGR
AGREE MENTW ITHTR UKEYE NDTHE CYPRU STHAT THEGR
EEKAN DTURK ISHCO NTING ENTSW HICHA RETOP ARTIC
IPATE INTHE TRIPA RTITE HEADQ UARTE RSSHA LLCOM
PRISE RESPE CTIVE LYGRE EKOFF ICERS NONCO MMISS
IONED OFFIC ERSAN DMENA NDTUR KISHO FFICE RSNON
COMMI SSION EDOFF ICERS ANDME NTHEP RESID ENTAN
DVICE PRESI DENTO FTHER EPUBL ICOFC YPRUS ACTIN
GINAG REEME NTMAY REQUE STTHE GREEK ANDTU RKISH
GOVER NMENT STOIN CREAS EORRE DUCET HEGRE EKAND
TURKI SHCON TINGE NTSIT ISAGR EEDTH ATTHE SITES
OFTHE CANTO NMENT SFORT HEGRE EKAND TURKI SHCON
TINGE NTSPA RTICI PATIN GINTH ETRIP ARTIT EHEAD
QUART ERSTH EIRJU RIDIC ALSTA TUSFA CILIT IESAN
DEXEM PTION SINRE SPECT OFCUS TOMSA NDTAX ESASW
ELLAS OTHER IMMUN ITIES ANDPR IVILE GESAN DANYO
THERM ILITA RYAND TECHN ICALQ UESTI ONSCO NCERN
INGTH EORGA NIZAT IONAN DOPER ATION OFTHE HEADQ
UARTE RSMEN TIONE DABOV ESHAL LBEDE TERMI NEDBY
ASPEC IALCO NVENT IONWH ICHSH ALLCO MEINT OFORC
ENOTL ATERT HANTH ETREA TYOFA LLIAN CE
"""
training_text = re.sub("[^A-Z]", "", training_text) # 只留A-Z
training_text = np.array(list(training_text))
training_text_len = len(training_text)
bi_gram = {}
tri_gram = {}

def training():
    for i in range(training_text_len - 2):
        if (training_text[i] + training_text[i + 1]) not in bi_gram:
            bi_gram[training_text[i] + training_text[i + 1]] = 0
        bi_gram[training_text[i] + training_text[i + 1]] += 1

        if (training_text[i] + training_text[i + 1] + training_text[i + 2]) not in tri_gram:
            tri_gram[training_text[i] + training_text[i + 1] + training_text[i + 2]] = 0
        tri_gram[training_text[i] + training_text[i + 1] + training_text[i + 2]] += 1

    if (training_text[training_text_len - 2] + training_text[training_text_len - 1]) not in bi_gram:
        bi_gram[training_text[training_text_len - 2] + training_text[training_text_len - 1]] = 0
    bi_gram[training_text[training_text_len - 2] + training_text[training_text_len - 1]] += 1

    return bi_gram, tri_gram

def compute_difference(cypher_text, row_num, column_num):   # from quiz2 q1
    input_arr = np.array(list(cypher_text)).reshape(column_num, row_num).T    # 因為要轉置，所以reshape的時候col和row要相反
    aver = round(column_num * 0.4, 3)
    diff = 0

    for r in range(row_num):
        vowel_num = 0
        for c in range(column_num):
            if input_arr[r][c] in ('A', 'E', 'I', 'O', 'U'):
                vowel_num = vowel_num + 1
        diff = round(diff + abs(vowel_num - aver), 3)

    return diff

def compute_weight(given_col, test_col):
    weight = 0
    for i in range(given_col.shape[0]): # 因為是用[:, cur_col - 2: cur_col]去取，所以col傳進來後已經變橫的了，也就是2*n的矩陣
        if (given_col[i, 0] + given_col[i, 1] + test_col[i] not in tri_gram) or (given_col[i, 0] + given_col[i, 1] not in bi_gram):
            weight += 0

        else:
            weight += math.log(26 * tri_gram[given_col[i, 0] + given_col[i, 1] + test_col[i]] / bi_gram[given_col[i, 0] + given_col[i, 1]])

    return weight


def Markov_decision_process_decrypt(cypher_text, row_num, column_num):
    plaintext = np.array(list(cypher_text)).reshape(column_num, row_num).T    # 因為要轉置，所以reshape的時候col和row要相反
    
    # 因為助教hint說GRE開頭, 所以把矩陣調整成GRE開頭, 但因E有好幾個所以只抓GR去開頭
    for col in range(column_num):
        if plaintext[0, col] == "G":
            plaintext[:, [0, col]] = plaintext[:, [col, 0]]

        elif plaintext[0, col] == "R":
            plaintext[:, [1, col]] = plaintext[:, [col, 1]]

    for cur_col in range(2, column_num):    # 確定cur_col要放哪一行
        max_weight = 0

        # 因為cur_col前面的行都已確定，測試cur_col後面的即可
        for test_col in range(cur_col, column_num):
            weight = compute_weight(plaintext[:, cur_col - 2: cur_col], plaintext[:, test_col])
            if max_weight < weight:
                max_weight = weight
                plaintext[:, [cur_col, test_col]] = plaintext[:, [test_col, cur_col]]

    return ''.join([str(i) for i in plaintext.flat])    # flat用來把ndarray攤平；str把ndarray轉字串(若有[]會連[]一起被轉成字串)

if __name__ == "__main__":
    training()

    cypher_text = input()
    cypher_text = re.sub("[^A-Z]", "", cypher_text) # 只留A-Z
    cypher_text = np.array(list(cypher_text))

    # factor直接寫死, 懶得做因數分解
    factor1 = 7
    factor2 = 11

    # 同quiz2 q1
    if compute_difference(cypher_text, factor1, factor2) < compute_difference(cypher_text, factor2, factor1):
        row_num, column_num = factor1, factor2
    else:
        row_num, column_num = factor2, factor1

    plaintext = Markov_decision_process_decrypt(cypher_text, row_num, column_num)

    print(plaintext)
    
