# Maximum Number of Events That Can Be Attended II

[题目](https://leetcode.com/problems/maximum-number-of-events-that-can-be-attended-ii/)

又是那种不难看懂代码但是叫我自己写不如杀了我的题目。
```c#
//https://leetcode.com/problems/maximum-number-of-events-that-can-be-attended-ii/editorial/
//这次的editorial有5种解法，不过基本思想都是dp+binary search，区别在于binary search的优化程度和dp的方向。这个是采样区最佳
public class Solution 
{
        int[][] dp;
        public int MaxValue(int[][] events, int k)
        {
            Array.Sort(events, (a, b) => (a[0] - b[0])); //按照event的开始时间排序，方便下面bisectRight使用binary search快速找到下一个event
            dp = new int[k+1][];

            for (int i = 0; i < dp.Length; i++)
            {
                dp[i] = Enumerable.Repeat(-1, events.Length).ToArray(); //生成一个长度为events.Length且元素都是-1的数组
            }

            return dfs(0, k, events);
        }

        private int dfs(int curIndex, int count, int[][] events)
        {
            if (count == 0 || curIndex == events.Length) return 0; //count为能最多参加的event数量，等于0了就不会有接下来的逻辑了

            if (dp[count][curIndex]!=-1) return dp[count][curIndex]; //这个dp也算cache了，防止重复计算已经解决过的问题

            int nextIndex = bisectRight(events, events[curIndex][1]); //events[curIndex][1]是curIndex所对应event的结束时间。根据结束时间找到第一个开始时间大于结束时间的event
            //当前index的dp有两种选择。1:不参加当前event，去参加下一个event，能获取的最大值为dfs(curIndex + 1, count, events)。 2:参加当前event，能获取的最大值是events[curIndex][2]（当前event的value）+dfs(nextIndex, count - 1, events)（结束后的下一个event处能获取的最大值）
            dp[count][curIndex] = Math.Max(dfs(curIndex + 1, count, events), events[curIndex][2] + dfs(nextIndex, count - 1, events));
            return dp[count][curIndex];
        }

        public int bisectRight(int[][] events, int target)
        {
            int left = 0, right = events.Length;
            while (left < right)
            {
                int mid = (left + right) / 2;
                if (events[mid][0] <= target)
                {
                    left = mid + 1;
                }
                else
                {
                    right = mid;
                }
            }
            return left;
        } 
}
```
```
Runtime
231 ms
Beats
99.69%
Memory
72.5 MB
Beats
60.80%
```
所以把binary search和dp初始化的部分拿掉，发现关键逻辑只有dfs的那么几行。所以dp到底哪里难？一个难点可能是Math.Max那里的关系，还有一个可能只有我会这样：我感觉我还不是特别明白递归，我老是被这个dfs给绕进去了，就是想不明白这个value是怎么累加起来返回的。感觉递归就是处理好base case和值是怎么加的，然后递归它自己就把自己处理好了。