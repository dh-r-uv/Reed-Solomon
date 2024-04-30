import random
import math
import gmpy2

def mul(a,b):
    return gmpy2.mul(a,b)

def square(a):
    return gmpy2.square(a)

def add(a,b):
    return gmpy2.add(a,b)

def mod(a,b):
    return gmpy2.f_mod(a,b)

def floor_div(a,b):
    return gmpy2.floor_div(a,b)

def bit_length(a):
    return gmpy2.bit_length(a)
def big_int(a):
    return gmpy2.mpz(a)

def is_odd(a): 
    return gmpy2.is_odd(a)


def ctz(v):
    return bit_length((v & -v)) - 1

# def bin_egcd(a, b):
#     if b == 0:
#         x = big_int(0)
#         y = big_int(1)
#         #gcd is b
#         return x
#     elif a == 0:
#         x = big_int(1)
#         y = big_int(0)
#         #gcd is a
#         return y
#     shift = ctz(a | b)
#     rx, ry, sx, sy, tx, ty = a, b, big_int(1), big_int(0), big_int(0), big_int(1)
#     while rx != ry:
#         if is_odd(rx):
#             if rx > ry:
#                 rx = add(rx, -ry)
#                 sx = add(sx, -sy)
#                 tx = add(tx, -ty)
#             else:
               
#                 ry = add(ry, -rx)
#                 sy = add(sy, -sx)
#                 ty = add(ty, -tx)
#         else:
#             rx = floor_div(rx, 2)
#             if is_odd(sx) :
#                 sx = floor_div(add(sx, b), 2)
#                 tx = floor_div(add(tx, -a), 2)
#             else:
#                 sx = floor_div(sx, 2)
#                 tx = floor_div(tx, 2)
#     #gcd is rx*2^shift
#     return sx

def new_egcd(a, b):
    r, r_prime, e = a, b, big_int(0)
    e = ctz(r | r_prime)
    r = r>>e
    r_prime = r_prime>>e
    a, b = r, r_prime
    s, t, s_prime, t_prime = big_int(1), big_int(0), big_int(0), big_int(1)
    while(r_prime!=0):
        while(r%2==0):
            r = r>>1
            if(s%2==0 and t%2==0):
                s = s>>1
                t = t>>1
            else:
                s = add(s, b)>>1
                t = add(t, -a)>>1
        while(r_prime%2==0):
            r_prime = r_prime>>1
            if(s_prime%2==0 and t_prime%2==0):
                s_prime = s_prime>>1
                t_prime = t_prime>>1
            else:
                s_prime = add(s_prime, b)>>1
                t_prime = add(t_prime, -a)>>1
        if(r_prime<r):
            r, s, t, r_prime, s_prime, t_prime = r_prime, s_prime, t_prime, r, s, t
        r_prime, s_prime, t_prime = r_prime-r, s_prime-s, t_prime-t
    return s

def fast_pow(a, b, m):
    ans = big_int(1)
    while b:
        if is_odd(b):
            ans = mod(mul(ans, a), m)
        a = mod(square(a), m)
        b = floor_div(b, 2)
    return ans

def check_witness(a, s, d, n):
    x = fast_pow(a, d, n)
    if x == 1 or x == n-1:
        return False
    for i in range(s-1):
        x = mod(square(x), n)
        if x == 1:
            return True
        if x == n-1:
            return False
    return True

def MillerRabin(n, iter=10):
    if n < 4:
        return n == 2 or n == 3
    if n % 2 == 0:
        return False
    d = n - 1
    s = ctz(d)
    d >>= s
    for i in range(iter):
        a = 2 + random.randint(0, n-3)
        if check_witness(a, s, d, n):
            return False
    return True


primes = []
N = big_int(1)
P = big_int(1)
M = big_int('9'*100)
u = 0.4
k = 700
def Global_Setup():
    global N, P
    n = 10000000
    lp = [0] * (n+1)
    c = 0
    for i in range(2, n+1):
        if lp[i] == 0:
            lp[i] = i
            primes.append(i)
            c += 1
            if c > k:
                break
        for j in range(len(primes)):
            if i * primes[j] > n:
                break
            lp[i * primes[j]] = primes[j]
            if primes[j] == lp[i]:
                break
    primes.reverse()
    primes.pop()
    for prime in primes:
        N = mul(N, prime)
    for i in range(math.ceil(u*k)):
        P = mul(P, primes[i])
    


def Rational_reconstruction(n, b, R, T):
    r_cur = big_int(n)
    r_prev = big_int(b)
    s_cur = big_int(1)
    t_cur = big_int(0)
    s_old = big_int(0)
    t_old = big_int(1)
    while r_prev > R:
        q = floor_div(r_cur, r_prev)
        r_cur, r_prev = r_prev, r_cur - mul(q, r_prev)
        s_cur, s_old = s_old, s_cur - mul(q, s_old)
        t_cur, t_old = t_old, t_cur - mul(q, t_old)
    return r_prev, t_old, s_old

def reconstruct_CRT(a):
    soln = big_int(0)
    for x in a:
        Ni = floor_div(N, x[0])
        #y = bin_egcd(Ni, x[0])
        y = new_egcd(Ni, x[0])
        soln = mod(add(soln, mul(mul(Ni, y), x[1])), N)
    return mod(soln, N)

def Transmit(a):
    lmax = int(u*k)
    l = random.randint(0, lmax)
    corrupted = set()
    b = []
    for i in range(l):
        corrupted.add(random.randint(0, k-1))
    print("Corrupted Indices: ", corrupted)
    for i in range(k):
        if i in corrupted:
            b.append([a[i][0], random.randint(0, a[i][0]-1)])
        else:
            b.append([a[i][0], a[i][1]])
    return b




def ReedSolomonSend(a):
    ai = []
    for i in range(k):
        ai.append([primes[i], mod(a, primes[i])])
    return Transmit(ai)



def ReedSolomonReceive(b):
    B = reconstruct_CRT(b)
    print("Corrupted Message received: ", B)
    r, t, s = Rational_reconstruction(N, B, mul(M, P), P)
    # print(r, t, s)
    if mod(r, t):
        return -1
    else:
        return floor_div(r, t)
    


if __name__ == "__main__":
    # print("Enter the max bound of the message: ")
    # M = int(input())
    # print("Enter the fraction of corruption: ")
    # u = float(input())
    # print("Enter the number of primes: ")
    # k = int(input())
    Global_Setup()

    assert N > mul(mul(M, P), P)

    print("Global Setup Done")
    # print("Enter the message to be transmitted: ")
    # message = int(input())
    message = big_int(232053499999999999999999999)
    print("Transmitting message.........")
    a = ReedSolomonSend(message)
    message_rec = ReedSolomonReceive(a)
    print("Message after Reconstruction: ", message_rec)



