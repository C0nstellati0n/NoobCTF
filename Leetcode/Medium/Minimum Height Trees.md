# [Minimum Height Trees](https://leetcode.com/problems/minimum-height-trees)

不是拓扑排序都给我写出来了，结果最后一步懵了？？？
```c++
//采样区，细节上的一些实现比普通实现更快
// https://leetcode.com/problems/minimum-height-trees/solutions/827284/c-99-tc-with-explanation-using-bfs-top-sort 更好理解
class Solution {
public:
    vector<int> findMinHeightTrees(int n, vector<vector<int>>& edges) {
        if(n == 1) return {0};
        vector<pair<int,int>> connectInfo(n);
        // Info - first : acc of vertex
        //      - second: connect number
        for(auto& edge : edges)
        {
            connectInfo[edge[0]].first += edge[1];
            connectInfo[edge[0]].second++;
            connectInfo[edge[1]].first += edge[0];
            connectInfo[edge[1]].second++;
        }
        vector<int> NotRootVertex;
        for(int i = 0 ; i < n ; i++)
        {
            if(connectInfo[i].second == 1)
                NotRootVertex.push_back(i);
        }
        vector<int> newLeave;
        while(n > 2)
        {
            n -= NotRootVertex.size();
            newLeave.clear();
            for(int i = 0 ; i < NotRootVertex.size() ; i++)
            {
                connectInfo[connectInfo[NotRootVertex[i]].first].first -= NotRootVertex[i];
                connectInfo[connectInfo[NotRootVertex[i]].first].second--;

                if(connectInfo[connectInfo[NotRootVertex[i]].first].second == 1)
                    newLeave.push_back(connectInfo[NotRootVertex[i]].first);
            }
            NotRootVertex = newLeave;
        }
        return NotRootVertex;
    }
};
```
拓扑排序，但是无向图。看来说拓扑排序只能用在有向图的说法不准确啊。这题的思路是，先排除那些边缘上只有一条边连接着的node，一层一层排除到中间，最里面剩下的就是答案。这么一看思路其实挺清晰的，因为要找高度最低的树（其实是没环的无向图），很自然的一个想法是，root肯定在最中间，这样无论往哪边延伸都不会太高。而边缘的node由于太靠边，如果选其为root，延伸到另一个极端的边缘就太高了。那么拿什么标准评判一个node在不在边缘呢？答案是边的数量，或者说“度”。看看题目给的例子，边缘那些孤零零的node是不是确实只有一条边连着呢？

无论是什么树，能构成MHT的root要么两个，要么一个（参考discussion区`sk4142`的评论）。一个root的树去边去到最后，root的度为0；但是两个root的树去边去到最后，两个root会连在一起，度互相为1。这咋办？可以往前顺一步，在去边的过程中，root必定有一次度为1。如果到最后有一个node度为1且其邻居无法入队列（这块还是看代码比较好理解），邻居和自己必定都是root