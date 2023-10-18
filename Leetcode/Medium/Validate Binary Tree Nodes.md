# [Validate Binary Tree Nodes](https://leetcode.com/problems/validate-binary-tree-nodes)

是的我就是那个投机取巧的人
```c#
//https://leetcode.com/problems/validate-binary-tree-nodes/editorial
//union find
//还有bfs和dfs解法，但是都比较好理解
class UnionFind {
    private int n;
    private int[] parents;
    public int components;
    public UnionFind(int n) {
        this.n = n;
        parents = new int[n];
        components = n;
        for (int i = 0; i < n; i++) {
            parents[i] = i;
        }
    }
    public bool union(int parent, int child) {
        int parentParent = find(parent);
        int childParent = find(child);
        if (childParent != child || parentParent == childParent) { //childParent==child是默认没有union时的情况；parentParent == childParent是两者已经连在一起的情况
            return false;
        }
        components--;
        parents[childParent] = parentParent;
        return true;
    }
    private int find(int node) {
        if (parents[node] != node) {
            parents[node] = find(parents[node]);
        }   
        return parents[node];
    }
}
class Solution {
    public bool ValidateBinaryTreeNodes(int n, int[] leftChild, int[] rightChild) {
        UnionFind uf = new UnionFind(n);
        for (int node = 0; node < n; node++) {
            int[] children = {leftChild[node], rightChild[node]};
            foreach(int child in children) {
                if (child == -1) {
                    continue;
                } 
                if (!uf.union(node, child)) { //node和child在union之前已经连在一起，说明有环
                    return false;
                }
            }
        }
        return uf.components == 1; //确保binary tree是连在一起而不是分开成几部分的。这个加上上面的无环隐含了A valid tree must have nodes with only one parent and exactly one node with no parent
    }
}
```
看到提示说`A valid tree must have nodes with only one parent and exactly one node with no parent.`我就立刻想到用字典。快快乐乐记完所有node检查各node只有一个parent且只有一个node无parent后，我提交——wrong answer。于是顿悟：万一是0->1->2->0，有环的binary tree我就没法检查了