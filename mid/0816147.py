import galois

# from quiz7
def modified_Berlekamp_Massey(seq):  #!!! 不知道why用這個方法時, input長度非2的倍數時會有錯
    s = list(seq)
    s = [int(i) for i in s]
    r = [1] + [0] * len(s)

    GF = galois.GF(2)
    s = galois.Poly(s)
    r = galois.Poly(r)

    return Extended_Euclidean_on_polynomial(r, s)

def Extended_Euclidean_on_polynomial(A, B):
    a1, a2, b1, b2 = galois.Poly([1]), galois.Poly([0]), galois.Poly([0]), galois.Poly([1])
    gcd1, gcd2 = A, B
    a_new, b_new, gcd_new = a1, b1, gcd1

    while(b_new.degree <= gcd_new.degree): # 要用<=
        #!!! 算的時候好像可以直接用quotient = gcd1 // gcd2, 目前測試下來兩種方式答案都一樣
        #!!! 不知道why處理gcd1比gcd2小的情況反而會錯, 不知道是有寫錯還是其他問題 e.g.quiz7 q1的input
        quotient = [1] + [0] * (gcd1.degree - gcd2.degree)
        quotient = galois.Poly(quotient)

        gcd_new = gcd1 - gcd2 * quotient
        a_new = a1 - a2 * quotient
        b_new = b1 - b2 * quotient

        a1, b1, gcd1 = a2, b2, gcd2
        a2, b2, gcd2 = a_new, b_new, gcd_new
        
    return b2
# end of quiz7

xor_map = {"00": "0", "01": "1", "10": "1", "11": "0"}

def str_xor(input_str1, input_str2): # 假設兩個string長度一樣
    ans = ""
    for i in range(len(input_str1)):
        ans += xor_map[input_str1[i] + input_str2[i]]
    
    return ans

def str_nor(input_str): # 0變1，1變0
    ans = ""
    for i in input_str:
        if i == "1":
            ans += "0"
        else:
            ans += "1"

    return ans

def lfsr_gen(seed, poly_nonzero_degree, output_len):
    poly_list = [0] * (poly_nonzero_degree[0] + 1)
    for i in poly_nonzero_degree:
        poly_list[len(poly_list) - 1 - i] = 1   # 因為要反轉
    poly = ''.join(str(i) for i in poly_list) 

    current_state = seed
    output = ""
    for _ in range(output_len):
        output += current_state[0]

        current_state = current_state + "0"
        if current_state[0] == "1": # 這次shift之後會溢位的話才要計算xor
            current_state = str_xor(current_state, poly)

        current_state = current_state[1:]
        
    return output


if __name__ == "__main__":
    input_path = "ciphertext.bin"
    with open(input_path,"rb") as f:
        input = f.read()
    f.close()
    
    ciphertext = [bin(c)[2:].rjust(8,'0') for c in input]  # remove '0b' from string, fill 8 bits
    ciphertext = ''.join(ciphertext)
    
    left_shift_ciphertext = ciphertext[1:] + "0"
    xor_ciphertext = str_xor(ciphertext, left_shift_ciphertext)

    lfsr_max_len = 32
    all_poly = {}
    # 假設一段對話中會有很多silence的部分，所以對每段2*n都假設他是silence，取出來算Berlekamp_Massey，統計哪個poly出現最多次代表他有可能是真正對應的poly
    for i in range(len(xor_ciphertext) - lfsr_max_len * 2 - 1):
        xor_partial_key = str_nor(xor_ciphertext[i: i + lfsr_max_len * 2])

        # 假設key[0]是0或1，然後可以推出剩下的
        partial_key_1 = ["0"]
        partial_key_2 = ["1"]
        
        for char_key in xor_partial_key:
            partial_key_1.append(str_xor(partial_key_1[len(partial_key_1) - 1], char_key))
            partial_key_2.append(str_xor(partial_key_2[len(partial_key_2) - 1], char_key))

        # 刪掉最後一個，是多的，沒用
        partial_key_1.pop()
        partial_key_2.pop()

        poly = modified_Berlekamp_Massey(partial_key_1) # 因為傳進去之後會再被list()一次，所以直接傳list也可以
        if poly in all_poly:
            all_poly[poly] += 1
        else:
            all_poly[poly] = 1

        poly = modified_Berlekamp_Massey(partial_key_2)
        if poly in all_poly:
            all_poly[poly] += 1
        else:
            all_poly[poly] = 1
    
    max_count = 0
    for poly in all_poly:
        if all_poly[poly] > max_count:
            max_count = all_poly[poly]
            target_poly = poly  

    # 算出來的 target_poly = x^30 + x^6 + x^4 + x + 1
    # 1000000000000000000000001010011

    """
    只想測試下面的東西時用，才不用每次都重跑上面
    GF = galois.GF(2)
    target_poly = galois.Poly([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,1,1])
    """

    seed = ""
    for _ in range(target_poly.degree - 1):
        seed += "0"
    seed += "1"

    key = lfsr_gen(seed, target_poly.nonzero_degrees, 4096)
    plaintext = str_xor(ciphertext, key)

    output_path = "plaintext.bin"
    output_file = open(output_path, 'wb+')

    for i in range(0, len(plaintext), 8):
        one_byte = 0
        for j in range(8):
            one_byte = one_byte << 1
            one_byte += int(plaintext[i + j])
        
        output_file.write(bytes([one_byte]))

    output_file.close()