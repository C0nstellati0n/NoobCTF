# [Sum of Distances in Tree](https://leetcode.com/problems/sum-of-distances-in-tree)

沉默是今晚的康桥
```c++
//采样区
//思路和 https://leetcode.com/problems/sum-of-distances-in-tree/solutions/130583/c-java-python-pre-order-and-post-order-dfs-o-n ， https://leetcode.com/problems/sum-of-distances-in-tree/solutions/1308366/c-solution-using-dfs-with-explanation-o-n-time-complexity 差不多，但是更快
class Solution {
    int head[30010], end[60010], next[60010], idx;
    int siz[30010], n; //siz[i]表示子树i的node数量
    vector<int> ans;
    void add (int a, int b) {
        //通过head[a]可以获取到其idx，有了idx就可以通过end获取到对应的b
        //但是这个next很难理解，根据下面dfs的逻辑，应该是用来记录neighbour的？
        end[idx] = b, next[idx] = head[a], head[a] = idx++;
    }
public:
    vector<int> sumOfDistancesInTree(int n, vector<vector<int>>& edges) {
        memset(head, -1, 4 * n + 4);
        for (auto &edge : edges) {
            int a = edge[0], b = edge[1];
            add(a, b), add(b, a);
        }
        this -> n = n;
        this -> ans = vector<int> (n);
        dfs(0, -1, 0);
        dfs(0, -1);
        return ans;
    }
    void dfs(int u, int pre, int level) {
        ans[0] += level;
        siz[u] = 1;
        for (int e = head[u]; ~e; e = next[e]) {
            int v = end[e];
            if ((e ^ 1) != pre) {
                dfs(v, e, level + 1);
                siz[u] += siz[v];
            }
        }
    }
    void dfs(int u, int pre) {
        for (int e = head[u]; ~e; e = next[e]) {
            if ((e ^ 1) == pre) continue;
            int v = end[e];
            ans[v] = ans[u] + n - 2 * siz[v];
            dfs(v, e);
        }
    }
};
```
这题据说是个reroot dp。我是不懂，只能记在这里，等下次见再研究了