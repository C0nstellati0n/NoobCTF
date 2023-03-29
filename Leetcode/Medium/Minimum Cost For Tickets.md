# Minimum Cost For Tickets

[题目](https://leetcode.com/problems/minimum-cost-for-tickets/description/)

看着大佬们百花齐放的答案，惊觉我还是那个给我看思路都写不出来的废物。dp题，discussion区有人发了思路：

```
Create a set of travel days using the given "days" array.
Find the maximum day in the "days" array and add 1 to it. This will be the maximum day we need to consider for travel.
Create a DP array of size n (maximum day) and initialize it with zeros.
Traverse the DP array from day 1 to maximum day and for each day:
If the day is not a travel day, set the DP value equal to the DP value of the previous day.
If the day is a travel day, set the DP value to the minimum cost of:
buying a 1-day pass and adding its cost to the DP value of the previous day.
buying a 7-day pass and adding its cost to the DP value of the day 7 days before.
buying a 30-day pass and adding its cost to the DP value of the day 30 days before.
Return the DP value of the maximum day (n-1).
```

确实有很多人是按照这个思路写的，不过实现方式有些许不同。接下来请欣赏解法1：用while循环计算天数。

```c#
//https://leetcode.com/problems/minimum-cost-for-tickets/solutions/3349729/java-python-and-c-easy-solutions-with-exaplanation-look-at-once/
class Solution {
    public int MincostTickets(int[] days, int[] costs) {
        int n = days.Length;
        int[] dp = new int[n + 1];
        Array.Fill(dp, Int32.MaxValue);
        dp[0] = 0;
        
        for (int i = 1; i <= n; i++) {
            dp[i] = dp[i - 1] + costs[0]; // 1-day pass for current day
            
            int j = i - 1;
            while (j >= 0 && days[i - 1] - days[j] < 7) j--;
            dp[i] = Math.Min(dp[i], dp[j + 1] + costs[1]); // 7-day pass for current day
            
            j = i - 1;
            while (j >= 0 && days[i - 1] - days[j] < 30) j--;
            dp[i] = Math.Min(dp[i], dp[j + 1] + costs[2]); // 30-day pass for current day
        }
        
        return dp[n];
    }
}
```

```
Runtime
83 ms
Beats
82.9%
Memory
38.6 MB
Beats
31.34%
```

一位特立独行的大佬就是不用dp数组，用队列。

```c#
//https://leetcode.com/problems/minimum-cost-for-tickets/solutions/3349786/image-explanation-recursion-dp-dp-optimized-c-java-python/
class Solution {
    public int MincostTickets(int[] days, int[] costs) {
        Queue<int[]> last7 = new();
        Queue<int[]> last30 = new();
        int cost = 0;

        foreach(int d in days) {
            while (last7.Count!=0 && last7.Peek()[0] + 7 <= d) {
                last7.Dequeue();
            }
            while (last30.Count!=0 && last30.Peek()[0] + 30 <= d) {
                last30.Dequeue();
            }
            last7.Enqueue(new int[]{d, cost + costs[1]});
            last30.Enqueue(new int[]{d, cost + costs[2]});
            cost = Math.Min(cost + costs[0], Math.Min(last7.Peek()[1], last30.Peek()[1]));
        }
        return cost;
    }
}
```

```
Runtime
81 ms
Beats
91.4%
Memory
38.4 MB
Beats
70.15%
```

能看出和第一个解法的while循环有异曲同工之妙。一个加一个减，一个队列另一个双指针。接下来的解法又是遍历dp，但是倒着来。

```c#
//https://leetcode.com/problems/minimum-cost-for-tickets/solutions/3349875/c-simple-dp-solution-100-91-5/
class Solution {
    public int MincostTickets(int[] days, int[] costs) {
        int lastDay = days.Max();
        int[] dp=new int[lastDay + 2];
        Array.Fill(dp,-1);
        // needed a + 1 so that the ticket can also cover the last day
        dp[lastDay + 1] = 0; // no trips after the last day so price is 0

        foreach(int day in days) dp[day] = 0;

        for (int i = lastDay; i >= 0; i--) {
            // no trips that day, take the price of next day
            if (dp[i] == -1) dp[i] = dp[i + 1];
            else {
                dp[i] = dp[Math.Min(i + 1, lastDay + 1)] + costs[0]; // 1 day pass
                dp[i] = Math.Min(dp[i], dp[Math.Min(i + 7, lastDay + 1)] + costs[1]); // 7 day pass
                dp[i] = Math.Min(dp[i], dp[Math.Min(i + 30, lastDay + 1)] + costs[2]); // 30 day pass
            }
        }

        return dp[0];
    }
}
```

```
Runtime
85 ms
Beats
77.61%
Memory
38.2 MB
Beats
88.6%
```

更常见的想法应该是正着遍历的dp。

```c#
//https://leetcode.com/problems/minimum-cost-for-tickets/solutions/3349791/day-362-flow-chart-java-c-python-explained-intuition-algo-dry-run-proof/
public class Solution {
    public int MincostTickets(int[] days, int[] costs) {
        // Get the maximum day in the travel period
        int maxDay = days[days.Length - 1];
        
        // Initialize the DP array and mark the travel days
        int[] dp = new int[maxDay + 1];
        bool[] isTravelDay = new bool[maxDay + 1];
        foreach(int day in days) {
            isTravelDay[day] = true;
        }
        
        // Initialize the costs of different types of passes
        int oneDayPassCost = costs[0];
        int sevenDayPassCost = costs[1];
        int thirtyDayPassCost = costs[2];
        
        // Compute the minimum cost for each day from 1 to maxDay
        for (int i = 1; i <= maxDay; i++) {
            if (!isTravelDay[i]) {
                // If it's not a travel day, the cost is the same as the previous day
                dp[i] = dp[i - 1];
            } else {
                // If it's a travel day, try all three types of passes and choose the minimum cost
                int cost1 = dp[i - 1] + oneDayPassCost;
                int cost2 = dp[Math.Max(0, i - 7)] + sevenDayPassCost;
                int cost3 = dp[Math.Max(0, i - 30)] + thirtyDayPassCost;
                dp[i] = Math.Min(cost1, Math.Min(cost2, cost3));
            }
        }
        
        // Return the minimum cost for the entire travel period
        return dp[maxDay];
    }
}
```

```
Runtime
83 ms
Beats
82.9%
Memory
38.1 MB
Beats
88.6%
```