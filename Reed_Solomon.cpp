#include <bits/stdc++.h>
#include "bigint.h"
using namespace std;
 #define int __int128
 //#define int long long
#define pii pair<int, int>
#define vi vector<int>
#define vii vector<pii>
#define pb push_back
#define F first
#define S second
//#define int bigint


/*in/out of u128 setup start*/
__int128 read() {
    __int128 x = 0, f = 1;
    char ch = getchar();
    while (ch < '0' || ch > '9') {
        if (ch == '-') f = -1;
        ch = getchar();
    }
    while (ch >= '0' && ch <= '9') {
        x = x * 10 + ch - '0';
        ch = getchar();
    }
    return x * f;
}
void print(__int128 x) {
    if (x < 0) {
        putchar('-');
        x = -x;
    }
    if (x > 9) print(x / 10);
    putchar(x % 10 + '0');
}
/*in/out of u128 setup end*/


/*extra functions start*/
int bin_egcd(int a, int b, int &x, int &y) {
    if (a==0 || b==0){
        if(a!=0){x=1, y=0; return a;}
        else {x=0, y=1; return b;}
    }
    int shift = __builtin_ctz(a | b);
    int rx = a, ry = b;
    int sx = 1, sy = 0, tx = 0, ty = 1;
    int cnt=0;
    while(rx!=ry){
        cnt++;
        if(rx&1){
            if(rx>ry){
                rx = rx-ry;
                sx = sx-sy;
                tx = tx-ty;
            }
            else{
                ry = ry-rx;
                sy = sy-sx;
                ty = ty-tx;
            }
        }
        else{
            rx = rx>>1;
            if(sx&1 || sx&1){
                sx = (sx+b)>>1;
                tx = (tx-a)>>1;
            }
            else{
                sx = sx>>1;
                tx = tx>>1;
            }
        }
    }
    x = sx;
    y = tx;
    return rx << shift;
}
//egcd that does rational reconstruction
void Rational_reconstruction(int n, int b, int R, int T, int &r, int &t, int &s){
    int r_cur = n, r_prev = b;
    int s_cur = 1, t_cur = 0, s_old = 0, t_old = 1;
    while(r_prev>R){
        int q = r_cur/r_prev;
        tie(r_cur, r_prev) = make_tuple(r_prev, r_cur-q*r_prev);
        tie(s_cur, s_old) = make_tuple(s_old, s_cur-q*s_old);
        tie(t_cur, t_old) = make_tuple(t_old, t_cur-q*t_old);
    }
    r = r_prev, s = s_old, t = t_old;
}

int reconstruct_CRT(vector<pii> &a){
    int N = 1;
    for(auto x:a){
        N*=x.F;
    }
    int soln = 0;
    for(auto x:a){
        int Ni = N/x.F;
        int y, z;
        bin_egcd(Ni, x.F, y, z);
        soln = (soln + Ni*y*x.S)%N;
    }
    return soln%N;
}

/*extra functions end*/

/*Miller Rabin*/
 int fast_pow(int a, int b, int m){
    int ans = 1;
    while(b){
        if(b&1) ans = (ans*a)%m;
        a = (a*a)%m; b>>=1;
    }
    return ans;
}

bool check_witness(int a, int s, int d, int n){
    int x = fast_pow(a, d, n);
    if(x==1 || x==n-1) return false;
    for(int i=0; i<s-1; i++){
        x = (x*x)%n;
        if(x==1) return true;
        if(x==n-1) return false;
    }
    return true;
}

bool MillerRabin(int n, int iter = 10){
    if(n<4)
        return n==2 || n==3;
    if(n%2==0) return false;
    int d = n-1;
    int s = __builtin_ctz(d);
    d>>=s;

    for(int i=0; i<iter; i++){
        int a = 2 + rand()%(n-3); //checking if a is a witness
        if(check_witness(a, s, d, n))
            return false;
    }
    return true;
}

/*Miller Rabin end*/





/*Actual program Starts here*/
vi primes;

int M = 1000;
float u = 0.2;
int k = 10;
int N = 1;
int P = 1;


//input is A, M, u, k
void Global_Setup(){
    int n = 10000000;
    vi lp(n+1);
    int c = 0;
    for (int i=2; i <= n; ++i) {
        if (lp[i] == 0) {
            lp[i] = i;
            primes.push_back(i);
            c++;
            if(c>k) break;
        }
        for (int j = 0; i * primes[j] <= n; ++j) {
            lp[i * primes[j]] = primes[j];
            if (primes[j] == lp[i]) {
                break;
            }
        }
    }
    reverse(primes.begin(), primes.end()); // Reverse the elements in the 'primes' vector
    primes.pop_back();
    for(auto prime:primes){
        N*=prime;
    }
    for(int i=0; i<floor(u*k); i++){
        P*=primes[i];
    }
    assert(N>2*M*P*P);
}
vii Transmit(vii &a){
    int lmax = floor(u*k), l = rand()%(lmax+1);
    set<int> corrupted;
    vii b;
    for(int i=0; i<l; i++){
        corrupted.insert(rand()%k);
    }
    for(int i=0; i<k; i++){
        if(corrupted.count(i))
            b.pb({a[i].F, rand()%a[i].F});
        else 
            b.pb({a[i].F, a[i].S});        
    } 
    return b;
}

vii ReedSolomonSend(int a){
    vii ai;
    for(int i=0; i<k; i++){
        ai.pb({primes[i], a%primes[i]});
    }
    return Transmit(ai);    
}


int ReedSolomonReceive(vii &b){
    int B = reconstruct_CRT(b);
    //cout << "Corrupted Message received: " << B << "\n";
    cout << "Corrupted Message received: ";
    print(B);
    cout << "\n";
    int r, t, s;
    cout << "Reconstructing the Message......\n";
    Rational_reconstruction(N, B, M*P, P, r, t, s);
    if(r%t) return -1;
    else return r/t;    
}

int32_t main(){
    cout << "Enter the max bound of the message: ";
    //cin >> M;
    M = read();
    cout << "Enter the fraction of corruption: ";
    cin >> u;
    // u = read();
    cout << "Enter the number of primes: ";
    //cin >> k; 
    k = read();
    Global_Setup();
    cout << "Global Setup Done\n";
    cout << "Enter the message to be transmitted: ";
    int message;
    //cin >> message;
    message = read();
    cout << "Transmitting message.........\n";
    vii a = ReedSolomonSend(message);
    int message_rec = ReedSolomonReceive(a);
    cout<<"Message after Reconstruction: ";
    print(message_rec);
}
/*Actual program ends here*/