#include <bits/stdc++.h>
#include "bigint.h"
using namespace std;
#define pii pair<int, int>
#define vi vector<int>
#define vii vector<pii>
#define pb push_back
#define F first
#define S second

/*debug start*/
 void __print32_t(int32_t x) {cerr << x;}
void __print32_t(long x) {cerr << x;}
void __print32_t(long long x) {cerr << x;}
void __print32_t(unsigned x) {cerr << x;}
void __print32_t(unsigned long x) {cerr << x;}
void __print32_t(unsigned long long x) {cerr << x;}
void __print32_t(float x) {cerr << x;}
void __print32_t(double x) {cerr << x;}
void __print32_t(long double x) {cerr << x;}
void __print32_t(char x) {cerr << '\'' << x << '\'';}
void __print32_t(const char *x) {cerr << '\"' << x << '\"';}
void __print32_t(const string &x) {cerr << '\"' << x << '\"';}
void __print32_t(bool x) {cerr << (x ? "true" : "false");}
 
template<typename T, typename V>
void __print32_t(const pair<T, V> &x) {cerr << '{'; __print32_t(x.first); cerr << ','; __print32_t(x.second); cerr << '}';}
template<typename T>
void __print32_t(const T &x) {int32_t f = 0; cerr << '{'; for (auto &i: x) cerr << (f++ ? "," : ""), __print32_t(i); cerr << "}";}
void _print32_t() {cerr << "]\n";}
template <typename T, typename... V>
void _print32_t(T t, V... v) {__print32_t(t); if (sizeof...(v)) cerr << ", "; _print32_t(v...);}
#ifndef ONLINE_JUDGE
#define debug(x...) cerr << "[" << #x << "] = ["; _print32_t(x)
#else
#define debug(x...)
#endif
 /*debug end*/


//n > 2MP^2 to be able to recover it

string s;
bigint M;
void setM(){
    for(int i=0; i<50; i++) s.pb(rand()%10);
    M = bigint(s);
}

vi primes;




int bin_egcd(int a, int b, int &x, int &y) {
    if (!a || !b){
        if(a) x=1, y=0;
        else x=0, y=1;
        return a | b;
    }
    unsigned shift = __builtin_ctz(a | b);
    int rx = a, ry = b;
    int sx = 1, sy = 0, tx = 0, ty = 1;
    int cnt=0;
    while(rx!=ry){
        cnt++;
        debug(cnt, rx, ry, sx, sy, tx, ty);
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


int combine_CRT(vector<pii> &a){
    int n = a.size();
    int ans = 0;
    int M = 1;
    for(int i=0; i<n; i++){
        M *= a[i].first;
    }
    for(int i=0; i<n; i++){
        int Mi = M/a[i].first;
        int x, y;
        bin_egcd(Mi, a[i].first, x, y);
        ans += a[i].second*Mi*x;
    }
    return ans%M;
}

int main(){
    int x, y;
    cout << bin_egcd(20, 130, x,y) <<endl;
    cout << x << " "<< y<<endl;
}