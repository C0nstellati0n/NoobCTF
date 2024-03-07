# [ROPChain](https://challenges.reply.com/challenges/coding-teen/code-teen2020/detail/)

经典dp题，不算特别有特点或者很难的dp。但我冥冥之中感觉这题要求的东西还挺常见的，不如记下来，今后要用就直接抄（就这玩意都写了我将近一个小时,dp功底虽然还是差，但好歹能不看dp公式自己推出来了）
```c++
#include <iostream>
#include <string>
#include <unordered_map>
using namespace std;
int numTestcases,i,j,n,k,m,start,len;
string s,temp;
int dp[1002];
int ropchain(const unordered_map<string,bool>& map){
    for(start=0;start<s.length();start++){
        for(len=1;start+len<=s.length();len++){
            if(map.find(s.substr(start,len))!=map.end()){
                if(start==0||dp[start])
                    dp[start+len]=dp[start+len]?min(dp[start+len],dp[start]+1):dp[start]+1;
            }
        }
    }
    return dp[s.length()]?dp[s.length()]:-1;
}
void testcase(const int& index){
    for(j=0;j<1002;j++){
        dp[j]=0;
    }
    cin>>n;
    unordered_map<string,bool> map;
    cin>>s;
    for(k=0;k<n;k++){
        cin>>temp;
        map[temp]=true;
        for(m=1;m<temp.length();m++){
            map[temp.substr(m)]=true;
        }
    }
    cout<<"Case #"<<index<<": "<<ropchain(map)<<"\n";
}
int main()
{
    cin>>numTestcases;
    for(i=1;i<=numTestcases;i++){
        testcase(i);
    }
    return 0;
}
```