# Coin Change II

[题目](https://leetcode.com/problems/coin-change-ii/description/)

全体起立！第一个没有抄答案的dp题！不过仍不是自己独立找到的dp关系，参考了 https://algorithmist.com/wiki/Coin_change 。也是个进步对吧？
```c#
public class Solution {
    public int Change(int amount, int[] coins) {
        int[,] dp=new int[amount+1,coins.Length];
        for(int i=0;i<amount+1;i++){
            for(int j=0;j<coins.Length;j++){
                dp[i,j]=-1;
            }
        }
        return recur(amount,coins,coins.Length-1,dp);
    }
    public int recur(int amount,int[] coins,int index,int[,] dp){
        if(index<0||amount<0){
            return 0;
        }
        if(amount==0){
            return 1;
        }
        if(dp[amount,index]!=-1){
            return dp[amount,index];
        }
        return dp[amount,index]=recur(amount,coins,index-1,dp)+recur(amount-coins[index],coins,index,dp);
    }
}
```
```
Runtime
75 ms
Beats
95.83%
Memory
48.5 MB
Beats
25%
```
然后我发现就算递归很简单，遍历做法也不一定好改。比如这个我自己一时半会真想不出来咋改。2d dp比较容易理解，不过[editorial](https://leetcode.com/problems/coin-change-ii/editorial/)的空间优化做法个人觉得有点难懂。
```c#
class Solution {
    public int Change(int amount, int[] coins) {
        int n = coins.Length;
        int[] dp = new int[amount + 1]; //dp[i]表示当amount为i时，有多少种组合方式
        dp[0] = 1; //base case。amount为0时，固定一种组合方式
        for (int i = n - 1; i >= 0; i--) {
            //不用考虑j=1到j=coins[i]-1的情况，因为这是bottom up，1到coins[i]-1的value目前没有硬币的组合
            for (int j = coins[i]; j <= amount; j++) { //取出硬币j=coins[i]，要求j<=amount是因为当某个硬币的值大于amount时，加上它肯定无法组合出amount
                dp[j] += dp[j - coins[i]]; //这里有两种情况：选择忽视当前硬币和加上当前硬币。不过第一种情况的值已经存储在dp[j]里了（bottom up上来的时候还没算上j本身），第二种情况则在dp[j - coins[i]]中。所以直接+=就能包括两种情况了
            }
        }
        return dp[amount];
    }
}
```
```
Runtime
63 ms
Beats
100%
Memory
38.2 MB
Beats
90.48%
```