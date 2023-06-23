# Best Time to Buy and Sell Stock with Transaction Fee

[题目](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/description/)

这题在看了vote数第一的[思路分析](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/solutions/108870/most-consistent-ways-of-dealing-with-the-series-of-stock-problems/)后，更不懂了。估计是要把stock系列的都试过再看那个才会有收获。我懵懵懂懂的看了一遍后，只有一句话：“啊？这是medium？”于是我去看了别人的解。果然是dp，不过没我想的那么复杂。
```c#
//https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/solutions/108871/2-solutions-2-states-dp-solutions-clear-explanation/
public class Solution {
    public int MaxProfit(int[] prices, int fee) {
        if (prices.Length <= 1) return 0;
        int days = prices.Length;
        int[] buy = new int[days];
        int[] sell = new int[days];
        buy[0]=-prices[0]-fee; //base case：买第0个股票并在买时支付交易费用
        for (int i = 1; i<days; i++) {
            //两个数组的dp不同处在于状态（值）的改变从另一个数组加上来，而不是当前数组。这样交错赋值就不用担心交易时手上没股票或者股票超过1个的情况了。详情见： https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/editorial/ ，这种dp似乎被称为“two states dp"
            buy[i] = Math.Max(buy[i - 1], sell[i - 1] - prices[i] - fee); // keep the same as day i-1, or buy from sell status at day i-1
            sell[i] = Math.Max(sell[i - 1], buy[i - 1] + prices[i]); // keep the same as day i-1, or sell from buy status at day i-1
        }
        return sell[days - 1];
    }
}
```
```
Runtime
172 ms
Beats
99.5%
Memory
48.2 MB
Beats
78.10%
```
虽然说是没多复杂，但是理解起来跟别的dp不一样。以前看的dp都只有一个数组，这回有两个（也有人说跟状态机state machine有关系）。而且我越看越发现dp真的好神奇，你尽管想各个值之间的联系，剩下的交给base case。这么一套下来莫名其妙地答案就出来了。

然后是空间优化形式的dp。
```c#
//https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/solutions/3667440/beats-100-c-java-python-beginner-friendly/
class Solution {
    public int MaxProfit(int[] prices, int fee) {
        int buy = Int32.MinValue;
        int sell = 0;
        foreach(int price in prices) {
            buy = Math.Max(buy, sell - price);
            sell = Math.Max(sell, buy + price - fee);
        }
        return sell;
    }
}
```
```
Runtime
178 ms
Beats
97.14%
Memory
49.2 MB
Beats
36.19%
```
你问我为什么memory数据比没优化的还差?这得问leetcode的testcase了……

你甚至可以直接用贪心做法。
```c#
//https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/solutions/201603/python-greedy-is-good/
public class Solution {
    public int MaxProfit(int[] prices, int fee) {
        int n=prices.Length;
        if(n<2){
            return 0;
        }
        int ans=0;
        int minimum=prices[0];
        for(int i=1;i<n;i++){
            if(prices[i]<minimum){
                minimum=prices[i];
            }
            else if(prices[i]>minimum+fee){
                ans+=prices[i]-fee-minimum;
                minimum=prices[i]-fee;
            }
        }
        return ans;
    }
}
```
```
Runtime
184 ms
Beats
87.62%
Memory
49.2 MB
Beats
45.71%
```