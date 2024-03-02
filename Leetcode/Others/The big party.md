# [The big party](https://challenges.reply.com/challenges/coding-teen/teen-edition-code-challenge/detail/)

对dijkstra的理解增加了！

简述一下这题的要求。一个带边权重和node权重的图有n个node，目标是举行k个派对。在每个node都可以举行任意数量的派对，但是不能连续固定在同一个node举行两次派对（也就是在node 2举行派对后要走到node 1或者别的什么相邻的node，然后再走回去就能再举行一次了）。走一条边要花费相应边的权重，在一个node上举行派对要花费node上的权重。从node 0出发，问怎么才能举行k个派对后再回到node 0？

我看到权重图的第一个反应就是dijkstra。然后又仔细看了几眼，嗯，怎么除了边有权重node还有权重啊？诶你举行派对还要走来走去？哇你还要返回起点？于是我就以为dijkstra用不了。事实证明大部分条件都是障眼法，权重图用dijkstra准没错
```c++
//参考了 https://challenges.reply.com/challenges/coding-teen/teen-edition-code-challenge/stats/ 里第一名队伍的代码
//重命名了变量，也自己写（抄）了一遍，方便理解
#include <iostream>
#include <fstream>
#include <queue>
#include <climits>
using namespace std;
int nmax=1001;
vector<vector<int>> min_dist(nmax,vector<int>(101)); //min_dist[i][j]记录算法在到达node i并已举办j个party时的weight（distance）
vector<vector<pair<int,int>>> adj_list(nmax);
vector<int> partyCost(nmax);
int numTestcases,dist,node,partyCount,neighbour,numParties,n,m,x,y,z,i,j;
struct nodeee //nodeee是一个方便编码的数据struct
{
    int dist,node,partyCount;
};
struct cmp
{
    bool operator ()(nodeee first,nodeee second)
    {
        return first.dist>second.dist;
    }
};
priority_queue<nodeee,vector<nodeee>,cmp> pq; //自定义排序函数排序结构
int dijkstra(){
    while(!pq.empty()) pq.pop();
    for(i=0;i<n;i++){
        for(j=0;j<=numParties;j++){
            min_dist[i][j]=INT_MAX;
        }
    }
    //node 0本身也可以举行一次party，那我们出发前到底举不举行一次？答案是都试一遍，哪个更好留给未来决定
    min_dist[0][0]=0;
    pq.push({0,0,0});
    min_dist[0][1]=partyCost[0];
    pq.push({partyCost[0],0,1});
    while(!pq.empty()){
        dist=pq.top().dist;
        node=pq.top().node;
        partyCount=pq.top().partyCount;
        pq.pop();
        if(dist<=min_dist[node][partyCount]){ //看了大佬的解法，这里写==也行。不过我直接根据（抄）之前写过的dijkstra算法写了<=，也行
            if(node==0&&partyCount==numParties) return dist; //已回到起点并已举办要求数量的party，直接返回
            for(int i=0;i<adj_list[node].size();i++){
                neighbour=adj_list[node][i].first;
                //这道题的一个小坑：它只说不能在连续固定地在同一个node举行两次派对，没说不能在两个相邻的node举行派对。而我们遍历当前node的neighbour时，绝对不会有自己，所以这个条件压根不用考虑
                //然后又是老生常谈的问题：下一个node上到底举不举行派对？答案我们早就知道了，都试一遍
                if(dist+adj_list[node][i].second<min_dist[neighbour][partyCount]){
                    min_dist[neighbour][partyCount]=dist+adj_list[node][i].second;
                    pq.push({min_dist[neighbour][partyCount],neighbour,partyCount});
                }
                if(dist+adj_list[node][i].second+partyCost[neighbour]<min_dist[neighbour][partyCount+1]){
                    min_dist[neighbour][partyCount+1]=dist+adj_list[node][i].second+partyCost[neighbour];
                    pq.push({min_dist[neighbour][partyCount+1],neighbour,partyCount+1});
                }
            }
        }
    }
    return INT_MAX;
}
int main()
{
    cin>>numTestcases;
    for(int cnt=1;cnt<=numTestcases;cnt++)
    {
        cin>>n>>m>>numParties;
        for(i=0;i<n;i++)
            cin>>partyCost[i];
        for(i=1;i<=m;i++)
        {
            cin>>x>>y>>z;
            //初始化临接表，{edge_to_connect,weight}
            adj_list[x].push_back({y,z});
            adj_list[y].push_back({x,z});
        }
        cout<<"Case #"<<cnt<<": "<<dijkstra()<<'\n';
        for(i=0;i<n;i++)
            adj_list[i].clear();
    }
    return 0;
}
```
本身不是很喜欢算法的，但是这题给我做爽了。就喜欢这种自己做不出来但是又有点基础所以能理解的；说难但其实也不难但自己想不出来的题