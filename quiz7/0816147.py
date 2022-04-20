import numpy as np
import galois

def Berlekamp_Massey(seq):
    s = list(seq)
    s = [int(i) for i in s]
    r = [1] + [0] * len(s)

    GF = galois.GF(2)
    s = galois.Poly(s)
    r = galois.Poly(r)
    print(r, s)
    print(Extended_Euclidean_on_polynomial(r, s))

def Extended_Euclidean_on_polynomial(A, B):
    a1, a2, b1, b2 = galois.Poly([1]), galois.Poly([0]), galois.Poly([0]), galois.Poly([1])
    gcd1, gcd2 = A, B
    a_new, b_new, gcd_new = a1, b1, gcd1

    print(a1, b1, gcd1, '\n', a2, b2, gcd2)
    """
    R0 = A
    R1 = B
    V0 = galois.Poly([0])
    V1 = galois.Poly([1])
    while(B.degree / 2 <= R1.degree):
        Q, R = R0 // R1, R0 % R1
        V = V0 - Q * V1
        V0 = V1
        V1 = V
        R0 = R1
        R1 = R

    print([1] + [0] * V1.degree)
    print(galois.Poly([1] + [0] * (V1.degree - 1)))
    return V1
    """
    """
    while(b_new.degree < gcd_new.degree):
        if gcd1.degree < gcd2.degree:
            quotient = gcd1 // gcd2
            gcd_new = gcd1 - gcd2 * quotient
            a_new = a1 - a2 * quotient
            b_new = b1 - b2 * quotient

        else:
            quotient = gcd1 // gcd2
            gcd_new = gcd1 - gcd2 * quotient
            a_new = a1 - a2 * quotient
            b_new = b1 - b2 * quotient

        a1, b1, gcd1 = a2, b2, gcd2
        a2, b2, gcd2 = a_new, b_new, gcd_new
        print(f'{quotient}\n{a_new}\n{b_new}\n{gcd_new}\n\n\n')

    print(f'{a2}\n{A}\n{b2}\n{B}\n{a2 * A}\n{b2 * B}\n{b2 * B}\n{b2 * B % A}\n{b2 * B % a2}\n{a2 * b2}\n')
        
    return a2 * A + b2 * B
    """
    """
    while(b_new.degree <= gcd_new.degree):
        quotient = gcd1 // gcd2

        gcd_new = gcd1 - gcd2 * quotient
        a_new = a1 - a2 * quotient
        b_new = b1 - b2 * quotient

        a1, b1, gcd1 = a2, b2, gcd2
        a2, b2, gcd2 = a_new, b_new, gcd_new
        print(f'{quotient}\n{a_new}\n{b_new}\n{gcd_new}\n\n\n')

    print(f'{a2}\n{A}\n{b2}\n{B}\n{a2 * A}\n{b2 * B}\n{b2 * B}\n{b2 * B % A}\n{b2 * B % a2}\n{a2 * b2}\n')
        
    return b2
    """
    while(b_new.degree <= gcd_new.degree):
        quotient = [1] + [0] * (gcd1.degree - gcd2.degree)
        quotient = galois.Poly(quotient)

        gcd_new = gcd1 - gcd2 * quotient
        a_new = a1 - a2 * quotient
        b_new = b1 - b2 * quotient

        a1, b1, gcd1 = a2, b2, gcd2
        a2, b2, gcd2 = a_new, b_new, gcd_new
        print(f'{quotient}\n{a_new}\n{b_new}\n{gcd_new}\n\n\n')

    print(f'{a2}\n{A}\n{b2}\n{B}\n{a2 * A}\n{b2 * B}\n{b2 * B}\n{b2 * B % A}\n{b2 * B % a2}\n{a2 * b2}\n')
        
    return b2
    """
    while(b_new.degree <= gcd_new.degree):
        quotient = [1] + [0] * (abs(gcd1.degree - gcd2.degree))
        quotient = galois.Poly(quotient)

        if gcd1.degree < gcd2.degree:
            gcd_new = gcd2 - gcd1 * quotient
            a_new = a2 - a1 * quotient
            b_new = b2 - b1 * quotient
        else:
            gcd_new = gcd1 - gcd2 * quotient
            a_new = a1 - a2 * quotient
            b_new = b1 - b2 * quotient

        a1, b1, gcd1 = a2, b2, gcd2
        a2, b2, gcd2 = a_new, b_new, gcd_new
        print(f'{quotient}\n{a_new}\n{b_new}\n{gcd_new}\n\n\n')
        
    return b2
    """

if __name__ == "__main__":
    seq = input()
    #seq = ''.join(reversed(seq))
    Berlekamp_Massey(seq)