# Climbing Stairs

[题目](https://leetcode.com/problems/climbing-stairs/description/)

爬n阶楼梯，1次可以走2步或者1步，问有多少种爬法？知识盲区，大脑在这之前只知道枚举的做法，连试都不用试就可以知道肯定不行。让我们看看万能的评论区有什么高见：

第一种，记忆递归。单纯递归所需时间呈指数级增长，不记忆之前已经求过的答案肯定会超运行时间。

```c#
public class Solution {
    public int ClimbStairs(int n) {
        List<int> dp=new(); //fill all values with -1
        for(int i=0;i<n+1;i++){
            dp.Add(-1); //源代码是c++，可以直接vector<int>dp(n+1,-1); 初始化值。没找到c#的list的类似语法，只能自己加了。感觉拖累运行时间
        }
        return findWays(n,dp);
    }
    int findWays(int n, List<int> dp)
    {
        if (n <= 1) return 1;
        if (dp[n] != -1) return dp[n];//already solved subproblems
        return dp[n]=findWays(n - 1, dp) + findWays(n - 2, dp); //store the result of subproblem in dp array
    }
}
```

```
Runtime
30 ms
Beats
26.28%
Memory
26.9 MB
Beats
12.7%
```

爬阶梯的递归实现和斐波那契数列完全一致。试想n阶台阶，我们有两种登上n阶台阶的可能：从第n-1阶来或者从第n-2阶台阶来。那登上n-1或者n-2阶台阶又有几种方式？n-1:n-1-1，n-1-2；n-2:n-2-1，n-2-2。类似地，我们这样递归下去，直到n变为1以下。1阶台阶不用多想，肯定只有一种走法。根据基本的递归思想再加上个用于存放之前求过的答案的dp数组，就是该解法了。

第二种，[动态规划](https://www.zhihu.com/question/23995189)（Dynamic Programming，也可以看看这篇[文章](https://zhuanlan.zhihu.com/p/91582909)）。

```c#
public class Solution {
    public int ClimbStairs(int n) {
        List<int> dp=new();
        for(int i=0;i<n+1;i++){
            dp.Add(-1);
        }
        dp[0]=1;
        dp[1]=1; //base cases
        for(int i=2;i<=n;++i){
            dp[i]=dp[i-1]+dp[i-2];
        }
        return dp[n];
    }
}
```

```
Runtime
22 ms
Beats
79.8%
Memory
27 MB
Beats
10.64%
```

具体思路跟上一种解法差不多，只不过这次我们不递归了。我们直接遍历dp数组，从非基本情况i=2开始，全部算出从2到n的答案，然后返回dp[n]就行了。

第三种，dp解法优化所用空间后的结果。

```c#
public class Solution {
    public int ClimbStairs(int n) {
        int prev2=1,prev1=1; //initally at 0th and 1st index
        int curr;
        for(int i=2;i<=n;i++){
            curr=prev1+prev2;
            prev2=prev1; //update pointers
            prev1=curr;
        }
        return prev1;
    }
}
```

```
Runtime
15 ms
Beats
98.84%
Memory
26.7 MB
Beats
31.99%
```

dp解法表现已经很不错了，只是每次都要存个长n+1的数组，有点浪费空间；况且我还要循环赋初始值，运行时间也慢了。不如我们只要3个变量，分别对应dp[i],dp[i-1],dp[i-2]的值，然后一边增加i，一边更新这些变量，i增加到n时返回curr（因为for循环最后把prev1赋值为curr，所以是`return prev1`）不就行了吗？结果确实也不错。