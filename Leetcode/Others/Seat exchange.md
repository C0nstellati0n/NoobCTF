# [Seat exchange](https://challenges.reply.com/challenges/coding-teen/code-teen-2021/detail/)

图论还在追我！它都踩我脸上了我才发现！

这题的描述也很简单，给出一个固定的置换（感觉和[这里](https://oi-wiki.org/math/permutation/)的定义差不多），返回置换k次后的结果。直接爆破（程序模拟置换k次）就能解决前4个testcase，但是第5个testcase因为k太大，会TLE

更好的方式是，将置换看成有向图，然后找里面的环。比如这个置换：`0 4 3 1 2`，0换到0的位置；1换到4的位置；2换到3的位置……不难看出，1->4->2->3->1,这是个圈。无论k有多大，1最后一定会落在索引1，4，2，3之中。具体是哪个也很好算，这个圈长度为4，最后的位置为`res[cycles[(0+k)%4]]=cycles[0]`。如果是4，4在这个圈的索引1处，因此最后的位置为`res[cycles[(1+k)%4]]=cycles[1]`。公式为`res[cycles[(i+k)%cycles.size()]]=cycles[i]`
```c++
#include <iostream>
#include <vector>
using namespace std;
int numTestcases,n,k,i,j,m;
int permutations[100001];
void calculate(){
    vector<int> ans(n);
    vector<bool> vis(n);
    for(int no=0;no<n;no++){
        if(vis[no]) continue;
        vector<int> cycles;
        int node=no;
        do{
            vis[node]=true;
            cycles.push_back(node);
            node=permutations[node];
        }
        while (node!=no);
        for(j=0;j<cycles.size();j++){
            ans[cycles[(j+k)%cycles.size()]]=cycles[j];
        }
    }
    for(j=0;j<n;j++){
        cout<<" "<<ans[j];
    }
}
void testcase(const int& index){
    cin>>n>>k;
    for(j=0;j<n;j++){
        cin>>permutations[j];
    }
    cout<<"Case #"<<index<<":";
    calculate();
    cout<<"\n";
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
看了这个[解析](https://www.youtube.com/watch?v=D9h6ONgxP9Q)才知道这种方法。还是太菜了