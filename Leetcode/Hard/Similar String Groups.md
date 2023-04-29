# Similar String Groups

[题目](https://leetcode.com/problems/similar-string-groups/description/)

兜兜转转还是回到dfs，bfs与union find的怀抱。

```c#
//dfs
//https://leetcode.com/problems/similar-string-groups/solutions/3462133/image-explanation-easy-to-understand-concise-c-java-python/
class Solution {
    public int NumSimilarGroups(string[] strs) {
        int groups = 0, n = strs.Length;
        bool[] vis = new bool[n];
        for(int i = 0; i < strs.Length; i++){
            if(vis[i]) continue;
            groups++;
            dfs(i, strs, vis);
        }
        return groups;
    }

    void dfs(int i, string[] strs, bool[] vis){
        vis[i] = true;
        for(int j = 0; j < strs.Length; j++){
            if(vis[j]) continue;
            if(isSimilar(strs[i], strs[j])){
                dfs(j, strs, vis);
            }
        }
    }

    bool isSimilar(string a, string b){
        int count = 0;
        for(int i = 0; i < a.Length; i++){
            if(a[i] != b[i]) count++;
        }
        return (count == 2 || count == 0); //如果正好有两个字符不一样，这两个字符就能交换从而是相似字符串。注意constraints里面的“All words in strs have the same length and are anagrams of each other.”
    }
}
```

```
Runtime
109 ms
Beats
75%
Memory
40.8 MB
Beats
100%
```

```c#
//bfs
class Solution {
    public void bfs(int node, Dictionary<int, List<int>> adj, bool[] visit) {
        Queue<int> q = new();
        q.Enqueue(node);
        visit[node] = true;
        while (q.Count!=0) {
            node = q.Dequeue();
            if (!adj.ContainsKey(node)) {
                continue;
            }
            foreach(int neighbor in adj[node]) {
                if (!visit[neighbor]) {
                    visit[neighbor] = true;
                    q.Enqueue(neighbor);
                }
            }
        }
    }

    public bool isSimilar(string a, string b) {
        int diff = 0;
        for (int i = 0; i < a.Length; i++) {
            if (a[i] != b[i]) {
                diff++;
            }
        }
        return diff == 0 || diff == 2;
    }

    public int NumSimilarGroups(string[] strs) {
        int n = strs.Length;
        Dictionary<int, List<int>> adj = new();
        // Form the required graph from the given strings array.
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (isSimilar(strs[i], strs[j])) {
                    if(!adj.ContainsKey(i)){
                        adj[i]=new();
                    }
                    if(!adj.ContainsKey(j)){
                        adj[j]=new();
                    }
                    adj[i].Add(j);
                    adj[j].Add(i);
                }
            }
        }

        bool[] visit = new bool[n];
        int count = 0;
        // Count the number of connected components.
        for (int i = 0; i < n; i++) {
            if (!visit[i]) {
                bfs(i, adj, visit);
                count++;
            }
        }

        return count;
    }
}
```

```
Runtime
118 ms
Beats
50%
Memory
41.7 MB
Beats
16.67%
```

```c#
//union find
//https://leetcode.com/problems/similar-string-groups/solutions/3462033/python-java-c-simple-solution-easy-to-understand/
class Solution {
    class UnionFind {
        int[] parent, rank;
        int count;

        public UnionFind(int n) {
            parent = new int[n];
            rank = new int[n];
            count = n;

            for (int i = 0; i < n; i++) {
                parent[i] = i;
            }
        }

        public int find(int x) {
            if (parent[x] != x) {
                parent[x] = find(parent[x]);
            }
            return parent[x];
        }

        public bool union(int x, int y) {
            int rootX = find(x);
            int rootY = find(y);

            if (rootX == rootY) {
                return false;
            }

            if (rank[rootX] < rank[rootY]) {
                int temp = rootX;
                rootX = rootY;
                rootY = temp;
            }

            parent[rootY] = rootX;

            if (rank[rootX] == rank[rootY]) {
                rank[rootX]++;
            }

            count--;

            return true;
        }

        public int getCount() {
            return count;
        }
    }

    public int NumSimilarGroups(string[] strs) {
        int n = strs.Length;
        UnionFind uf = new UnionFind(n);

        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (isSimilar(strs[i], strs[j])) {
                    uf.union(i, j);
                }
            }
        }

        return uf.getCount();
    }

    private bool isSimilar(string s1, string s2) {
        if (s1==s2) {
            return true;
        }

        int diff = 0;
        for (int i = 0; i < s1.Length; i++) {
            if (s1[i] != s2[i]) {
                diff++;
                if (diff > 2) {
                    return false;
                }
            }
        }

        return diff == 2;
    }
}
```

```
Runtime
86 ms
Beats
91.67%
Memory
41.3 MB
Beats
41.67%
```

感觉有点像找岛屿数量的那道题。把相似的字符串看作连在一起的岛屿，isSimilar函数判断是否连着，如果连着就继续遍历。最外层的遍历计数。