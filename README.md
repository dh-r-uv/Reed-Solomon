# REED SOLOMON ERROR CORRECTION IMPLEMENTATION

Reed-Solomon (RS) is an error correction code that is widely used in various applications, including data storage, wireless communication, and digital broadcasting. It is designed to detect and correct errors in transmitted or stored data.


## SETUP

- Fork the repo

- Run ``` pip install gympy2``` on your terminal to install the gympy package to handle large number computations.

- Run ```python ReedSolomon2.py``` to run the file

## Files
- Reed_Solomon.py
- Reed_Solomon2.py: handles big integers using gmpy2 
- Reed_Solomon.cpp: cpp version for the same

### Primary Functions

- Binary EGCD
``` python
def new_egcd(a, b):
    r, r_prime, e = a, b, big_int(0)
    e = ctz(r | r_prime)
    r = r>>e
    r_prime = r_prime>>e
    a, b = r, r_prime
    s, t, s_prime, t_prime = big_int(1), big_int(0), big_int(0), big_int(1)
    while(r_prime!=0):
        while(is_even(r)):
            r = r>>1
            if(is_even(s) and is_even(t)):
                s = s>>1
                t = t>>1
            else:
                s = add(s, b)>>1
                t = add(t, -a)>>1
        while(is_even(r_prime)):
            r_prime = r_prime>>1
            if(is_even(s_prime) and is_even(t_prime)):
                s_prime = s_prime>>1
                t_prime = t_prime>>1
            else:
                s_prime = add(s_prime, b)>>1
                t_prime = add(t_prime, -a)>>1
        if(r_prime<r):
            r, s, t, r_prime, s_prime, t_prime = r_prime, s_prime, t_prime, r, s, t
        r_prime, s_prime, t_prime = r_prime-r, s_prime-s, t_prime-t
    return s
```

- CRT
```python 
    def reconstruct_CRT(a):
    soln = big_int(0)
    for x in a:
        Ni = floor_div(N, x[0])
        y = new_egcd(Ni, x[0])
        soln = mod(add(soln, mul(mul(Ni, y), x[1])), N)
    return mod(soln, N)
```

- Miller Rabin
```python 
def check_witness(a, s, d, n):
    x = big_int(fast_pow(a, d, n))
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
```

- Uses the theorem of rational reconstruction `https://en.wikipedia.org/wiki/Rational_reconstruction_(mathematics)`


### Usefulness:


Used to transfer data into many small packets over a non reliable line and retrieve the right data from it using the magic of Number theory

## Contributors:

Dhruv Kothari
Owais Mohammed





