# Longest ZigZag Path in a Binary Tree

[题目](https://leetcode.com/problems/longest-zigzag-path-in-a-binary-tree/description/)

做出来了，就是这运行速度……还以为要TLE。

```c#
public class Solution {
    public int LongestZigZag(TreeNode root) {
        List<int> res=new();
        Traverse(root,res);
        return res.Max();
    }
    int MaxZigZag(TreeNode node,int direction){
        int res=0;
        while(node!=null){
            if(direction==-1){
                node=node.left;
            }
            else{
                node=node.right;
            }
            res++;
            direction=-direction;
        }
        return res-1;
    }
    public void Traverse(TreeNode node,List<int> res){
        if(node==null){
            return;
        }
        Traverse(node.left,res);
        res.Add(MaxZigZag(node,-1));
        res.Add(MaxZigZag(node,1));
        Traverse(node.right,res);
    }
}
```

```
Runtime
3580 ms
Beats
25%
Memory
56 MB
Beats
75%
```

《3580 ms》。更离谱的是，这样都能超越25%，接下来的解法耗时骤降却也只能超越25%.

```c#
//https://leetcode.com/problems/longest-zigzag-path-in-a-binary-tree/solutions/3432994/python-java-c-simple-solution-easy-to-understand/
public class Solution {
    public int LongestZigZag(TreeNode root) {
        int[] res = dfs(root);
        return res[2];
    }
    
    private int[] dfs(TreeNode node) {
        if (node == null) {
            return new int[]{-1, -1, -1};
        }
        
        int[] leftSubtree = dfs(node.left);
        int[] rightSubtree = dfs(node.right);
        
        int leftLength = leftSubtree[1] + 1;
        int rightLength = rightSubtree[0] + 1;
        int maxLen = Math.Max(Math.Max(leftLength, rightLength), Math.Max(leftSubtree[2], rightSubtree[2]));
        
        return new int[]{leftLength, rightLength, maxLen};
    }
}
```

```
Runtime
250 ms
Beats
25%
Memory
65.4 MB
Beats
25%
```

基本都是dfs，只不过实现方式不一样。

```c#
//https://leetcode.com/problems/longest-zigzag-path-in-a-binary-tree/solutions/3433060/image-explanation-easy-complete-intuition-c-java-python/
class Solution {
    public int maxLength=0;
    public void solve(TreeNode root,bool dir,int currLength){
        if(root==null) return;
        maxLength=Math.Max(maxLength,currLength);
        if(dir){
            solve(root.left,false,currLength+1);
            solve(root.right,true,1);
        }
        else{
            solve(root.right,true,currLength+1);
            solve(root.left,false,1);
        }
    }

    public int LongestZigZag(TreeNode root) {
        solve(root,false,0);
        solve(root,true,0);
        return maxLength;
    }
}
```

```
Runtime
207 ms
Beats
25%
Memory
55.4 MB
Beats
75%
```

一个稀有的bfs，利用自己构建的另一个类。

```c#
//https://leetcode.com/problems/longest-zigzag-path-in-a-binary-tree/solutions/3433417/easy-solutions-in-java-python-and-c-look-at-once-with-exaplanation/
class Triplet {
    public TreeNode node;
    public int n;
    public int left;
    
    public Triplet(TreeNode node, int n, int left) {
        this.node = node;
        this.n = n;
        this.left = left;
    }
}
class Solution {
    public int LongestZigZag(TreeNode root) {
        int ans = 0;
        Stack<Triplet> stack = new();
        stack.Push(new Triplet(root, 0,0));
        while (stack.Count!=0) {
            Triplet triplet = stack.Pop();
            TreeNode node = triplet.node;
            int n = triplet.n;
            int left = triplet.left;
            if (node != null) {
                ans = Math.Max(ans, n);
                stack.Push(new Triplet(node.left, left != null && left == 0 ? n + 1 : 1, 1));
                stack.Push(new Triplet(node.right, left != null && left == 1 ? n + 1 : 1, 0));
            }
        }
        return ans;
    }
}
```

```
Runtime
208 ms
Beats
25%
Memory
58.2 MB
Beats
25%
```

代码最短的dfs。

```c#
//https://leetcode.com/problems/longest-zigzag-path-in-a-binary-tree/solutions/3433160/leetcode-the-hard-way-dfs-explained-line-by-line/
class Solution {
    int dfs(TreeNode root, bool isLeft, int cnt) {
        // root is nullptr, we can return `cnt`
        if (root==null) return cnt;
        // if `isLeft` is true, we have two choices
        // 1. go to right making a zipzag path - increase the cnt by 1 
        // 2. still go to left - starting a new zigzag path - hence cnt is set to 0
        if (isLeft) return Math.Max(dfs(root.right, false, cnt + 1), dfs(root.left, true, 0));
        // similarly, we apply the same logic for the opposite direction
        return Math.Max(dfs(root.left, true, cnt + 1), dfs(root.right, false, 0));
    }
    public int LongestZigZag(TreeNode root) {
        return Math.Max(dfs(root.left, true, 0), dfs(root.right, false, 0));
    }
}
```

```
Runtime
187 ms
Beats
75%
Memory
55.9 MB
Beats
75%
```

左右分开的dfs。

```c#
public class Solution {
    int max = 0;
    public int LongestZigZag(TreeNode root) {
        max = 0;
        zagLeft(root);
        zagRight(root);
        return max;
    }

    private int zagRight(TreeNode node)
    {
        if(node == null)
        {
            return 0;
        }
        int res = 0;
        if(node.left!=null)
        {
            res = 1 + zagLeft(node.left);
        }
        
        max = Math.Max(max,res);
        zagRight(node.left);
        return res;
    }
    private int zagLeft(TreeNode node)
    {
        if(node == null)
        {
            return 0;
        }
        int res = 0;
        if(node.right != null)
        {
            res = 1 + zagRight(node.right);
        }
        
        max = Math.Max(max,res);
        zagLeft(node.right);
        return res;
    }
}
```

```
Runtime
198 ms
Beats
50%
Memory
55.5 MB
Beats
75%
```