import galois

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

if __name__ == "__main__":
    seq = input() #!!! 有時就算input是2的倍數答案還有問題 e.g.10111110時會錯
    print(modified_Berlekamp_Massey(seq))