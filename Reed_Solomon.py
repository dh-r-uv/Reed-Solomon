import random

def ctz(v):
    return (v & -v).bit_length() - 1

def bin_egcd(a, b):
    if b == 0:
        x = 0
        y = 1
        return a
    elif a == 0:
        x = 1
        y = 0
        return b
    shift = ctz(a | b)
    rx, ry, sx, sy, tx, ty = a, b, 1, 0, 0, 1
    while rx != ry:
        if rx & 1:
            if rx > ry:
                rx = rx - ry
                sx = sx - sy
                tx = tx - ty
            else:
                ry = ry - rx
                sy = sy - sx
                ty = ty - tx
        else:
            rx = rx >> 1
            if sx & 1 or sx & 1:
                sx = (sx + b) >> 1
                tx = (tx - a) >> 1
            else:
                sx = sx >> 1
                tx = tx >> 1
    
    return sx

def fast_pow(a, b, m):
    ans = 1
    while b:
        if b & 1:
            ans = (ans * a) % m
        a = (a * a) % m
        b >>= 1
    return ans

def check_witness(a, s, d, n):
    x = fast_pow(a, d, n)
    if x == 1 or x == n-1:
        return False
    for i in range(s-1):
        x = (x*x)%n
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

# #define vi vector<int>
# vi primes;

# int M = 1000;
# float u = 0.2;
# int k = 10;
# int N = 1;
# int P = 1;


# input is A, M, u, k
# void Global_Setup(){
#     int n = 10000000;
#     vi lp(n+1);
#     int c = 0;
#     for (int i=2; i <= n; ++i) {
#         if (lp[i] == 0) {
#             lp[i] = i;
#             primes.push_back(i);
#             c++;
#             if(c>k) break;
#         }
#         for (int j = 0; i * primes[j] <= n; ++j) {
#             lp[i * primes[j]] = primes[j];
#             if (primes[j] == lp[i]) {
#                 break;
#             }
#         }
#     }
#     reverse(primes.begin(), primes.end()); // Reverse the elements in the 'primes' vector
#     primes.pop_back();
#     for(auto prime:primes){
#         N*=prime;
#     }
#     for(int i=0; i<floor(u*k); i++){
#         P*=primes[i];
#     }
#     assert(N>2*M*P*P);
# }

primes = []
N = 1
P = 1
M = int('9'*100)
u = 0.425
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
        N *= prime
    for i in range(int(u*k)):
        P *= primes[i]
    assert N > 2*M*P*P

# #def vii vector<vector<int>>
# vii Transmit(vii &a){
#     int lmax = floor(u*k), l = rand()%(lmax+1);
#     set<int> corrupted;
#     vii b;
#     for(int i=0; i<l; i++){
#         corrupted.insert(rand()%k);
#     }
#     for(int i=0; i<k; i++){
#         if(corrupted.count(i))
#             b.pb({a[i].F, rand()%a[i].F});
#         else 
#             b.pb({a[i].F, a[i].S});        
#     } 
#     return b;
# }

# void Rational_reconstruction(int n, int b, int R, int T, int &r, int &t, int &s){
#     int r_cur = n, r_prev = b;
#     int s_cur = 1, t_cur = 0, s_old = 0, t_old = 1;
#     while(r_prev>R){
#         int q = r_cur/r_prev;
#         tie(r_cur, r_prev) = make_tuple(r_prev, r_cur-q*r_prev);
#         tie(s_cur, s_old) = make_tuple(s_old, s_cur-q*s_old);
#         tie(t_cur, t_old) = make_tuple(t_old, t_cur-q*t_old);
#     }
#     r = r_prev, s = s_old, t = t_old;
# }

# int reconstruct_CRT(vector<pii> &a){
#     int N = 1;
#     for(auto x:a){
#         N*=x.F;
#     }
#     int soln = 0;
#     for(auto x:a){
#         int Ni = N/x.F;
#         int y, z;
#         bin_egcd(Ni, x.F, y, z);
#         soln = (soln + Ni*y*x.S)%N;
#     }
#     return soln%N;
# }

def Rational_reconstruction(n, b, R, T):
    r_cur = n
    r_prev = b
    s_cur = 1
    t_cur = 0
    s_old = 0
    t_old = 1
    while r_prev > R:
        q = r_cur // r_prev
        r_cur, r_prev = r_prev, r_cur - q * r_prev
        s_cur, s_old = s_old, s_cur - q * s_old
        t_cur, t_old = t_old, t_cur - q * t_old
    return r_prev, t_old, s_old

def reconstruct_CRT(a):
    N = 1
    for x in a:
        N *= x[0]
    soln = 0
    for x in a:
        Ni = N // x[0]
        y = bin_egcd(Ni, x[0])
        soln = (soln + Ni * y * x[1]) % N
    return soln % N

def Transmit(a):
    lmax = int(u*k)
    l = random.randint(0, lmax)
    corrupted = set()
    b = []
    for i in range(l):
        corrupted.add(random.randint(0, k-1))
    for i in range(k):
        if i in corrupted:
            b.append([a[i][0], random.randint(0, a[i][0]-1)])
        else:
            b.append([a[i][0], a[i][1]])
    return b


# vii ReedSolomonSend(int a){
#     vii ai;
#     for(int i=0; i<k; i++){
#         ai.pb({primes[i], a%primes[i]});
#     }
#     return Transmit(ai);    
# }

def ReedSolomonSend(a):
    ai = []
    for i in range(k):
        ai.append([primes[i], a % primes[i]])
    return Transmit(ai)

# int ReedSolomonReceive(vii &b){
#     int B = reconstruct_CRT(b);
#     //cout << "Corrupted Message received: " << B << "\n";
#     cout << "Corrupted Message received: ";
#     print(B);
#     cout << "\n";
#     int r, t, s;
#     cout << "Reconstructing the Message......\n";
#     Rational_reconstruction(N, B, M*P, P, r, t, s);
#     if(r%t) return -1;
#     else return r/t;    
# }

def ReedSolomonReceive(b):
    B = reconstruct_CRT(b)
    print("Corrupted Message received: ", B)
    r, t, s = Rational_reconstruction(N, B, M*P, P)
    print(r, t)
    if r % t:
        return -1
    else:
        return r // t
    
# int32_t main(){
#     cout << "Enter the max bound of the message: ";
#     //cin >> M;
#     M = read();
#     cout << "Enter the fraction of corruption: ";
#     cin >> u;
#     // u = read();
#     cout << "Enter the number of primes: ";
#     //cin >> k; 
#     k = read();
#     Global_Setup();
#     cout << "Global Setup Done\n";
#     cout << "Enter the message to be transmitted: ";
#     int message;
#     //cin >> message;
#     message = read();
#     cout << "Transmitting message.........\n";
#     vii a = ReedSolomonSend(message);
#     int message_rec = ReedSolomonReceive(a);
#     cout<<"Message after Reconstruction: ";
#     print(message_rec);
# }

if __name__ == "__main__":
    print("Enter the max bound of the message: ")
    # M = int(input())
    print("Enter the fraction of corruption: ")
    # u = float(input())
    print("Enter the number of primes: ")
    # k = int(input())
    Global_Setup()
    print("Global Setup Done")
    print("Enter the message to be transmitted: ")
    # message = int(input())
    message = 232053499999999999999999999
    print("Transmitting message.........")
    a = ReedSolomonSend(message)
    message_rec = ReedSolomonReceive(a)
    print("Message after Reconstruction: ", message_rec)
