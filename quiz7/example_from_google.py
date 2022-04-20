def BM(sequence): 
    f_min = [0]  #最低次多项式 
    l = [0]      #记录每一次最低次多项式次数 
    for i in range(len(sequence)):
        d = 0           
        for j in f_min:  #计算每一次的d值
            d += sequence[i+j-max(l)]  #mod问题、序列问题
        d = d %2            
        if d == 0:       #d为0时
            l.append(l[i])     
        else:            #d不为0时
            if the_same(l):       #d不为0且l列表中数字相同时
                n = i
                fn = f_min.copy()           #copy问题
                f_min.append(i+1)
                l.append(i+1)
            else:                 #d不为0时且l列表中数字不同时 
                if max(f_min) > max(fn):  #用于记录m以及fm的值    
                    m = n 
                    fm = fn.copy()
                n = i
                fn = f_min.copy()
                if m-l[m] >= n-l[n]: 
                    f_min += [j+(m-l[m]-n+l[n]) for j in fm]
                else:
                    f_min = [j+(-m+l[m]+n-l[n]) for j in f_min] + fm
                l.append(max(f_min))     
    f_min = condense(f_min)                
    return f_min

def condense(f_min):    #压缩f多项式，即相同的阶数利用二元加法合并排序后返回 
    f = list(set(f_min))
    for i in f_min:
        if f_min.count(i) % 2 ==0:
            if i in f:
                f.remove(i)
    f = sorted(f, reverse=True)        
    return f

def the_same(l):           #判断l列表中的数字是否全部相同 
    for i in range(len(l)-1):
        if l[i]!=l[i+1]:        
            return False
    return True
 
def print_f(f_min):        #还原多项式字符串并返回
    result = ''     
    for i in f_min: 
        if i == 0: 
            result += '1' 
        else: 
            result += 'x^' + str(i) 
        if i != f_min[-1]: 
            result += '+' 
    return result 
 
def Seq2list(sequence):    #将字符串转为int形列表 
    result = [] 
    for i in sequence: 
        result.append(int(i)) 
    return result 

if __name__ == "__main__":
    seq = ['10110001', '1001', '10111110', '000011101101010001101111001011', '101011110100010010110111100010', '000000100000110000101000111100100010110011101010011111010000111000100100110110101101111011000110100101']
    for S in seq: 
        f_min = BM(Seq2list(S)) 
        print('输入序列：' + S)  
        print('最低次多项式：' + print_f(f_min)) 
        print('最低次数：' + str(max(f_min))) 
        print(" ")