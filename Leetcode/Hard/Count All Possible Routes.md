# Count All Possible Routes

[题目](https://leetcode.com/problems/count-all-possible-routes/description/)

这是我第一个没有直接拷贝答案的hard题。在看了hint+discussion的提示后了解到要用dfs+二维dp，然后在瞟了editorial无数次后写出一个能通过testcases但只能通过一点点的解，最后疯狂比对editorial找到bug最终ac。（啊这不还是抄答案吗？）
```c#
//https://leetcode.com/problems/count-all-possible-routes/editorial/
public class Solution {
    public int CountRoutes(int[] locations, int start, int finish, int fuel) {
        int[][] dp=new int[locations.Length][];
        for(int i=0;i<locations.Length;i++){
            int[] temp=new int[fuel+1]; //要+1，否则数组越界
            Array.Fill(temp,-1);
            dp[i]=temp;
        }
        return solve(locations,start,finish,dp,fuel);
    }
    int solve(int[] locations,int city,int finish,int[][] dp,int remainingFuel){
        if(remainingFuel<0){
            return 0;
        }
        if(dp[city][remainingFuel]!=-1){
            return dp[city][remainingFuel];
        }
        int ans=city==finish?1:0;
        for(int next=0;next<locations.Length;next++){
            if(next==city){
                continue;
            }
            ans=(ans+solve(locations,next,finish,dp,remainingFuel-Math.Abs(locations[city]-locations[next])))%1000000007; //注意必须要ans+solve后再模，只模solve然后加上ans的话不对
        }
        return dp[city][remainingFuel]=ans;
    }
}
```
```
Runtime
139 ms
Beats
83.33%
Memory
40.9 MB
Beats
83.33%
```
与普通dfs的区别在于没有visited标记走过的node，毕竟此题允许重复走，不用担心无限递归，因为fuel在不断减少。其他都还挺常规的。这题的dp数组我怎么感觉更像cache，防止重复计算之前已经算过的值，dfs爆破所有走法。

那么既然有递归做法就有不递归的做法。
```c#
class Solution {
    public  int CountRoutes(int[] locations, int start, int finish, int fuel) {
        int n = locations.Length;
        int[][] dp = new int[n][];
        for(int i=0;i<n;i++){
            int[] temp=new int[fuel+1];
            dp[i]=temp;
        }
        Array.Fill(dp[finish],1);
        int ans = 0;
        for (int j = 0; j <= fuel; j++) {
            for (int i = 0; i < n; i++) {
                for (int k = 0; k < n; k++) {
                    if (k == i) {
                        continue;
                    }
                    if (Math.Abs(locations[i] - locations[k]) <= j) {
                        dp[i][j] = (dp[i][j] + dp[k][j - Math.Abs(locations[i] - locations[k])]) %
                                   1000000007;
                    }
                }
            }
        }
        return dp[start][fuel];
    }
}
```
```
Runtime
244 ms
Beats
50%
Memory
40.8 MB
Beats
83.33%
```