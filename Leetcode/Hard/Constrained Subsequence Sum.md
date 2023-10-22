# [Constrained Subsequence Sum](https://leetcode.com/problems/constrained-subsequence-sum)

要么是leetcode疯了，要么是我疯了。怎么一个两个全是hard啊？这就是连续一周easy的代价吗？
```c#
//https://leetcode.com/problems/constrained-subsequence-sum/editorial
//Approach 1: Heap/Priority Queue
class Solution {
    //注意这题的k表示取subsequence时间隔不能超过k。比如[1,2,3,4],k=2，我们在4（index 3）。那么subsequence取了4后还能取3，2，1（index 0）不能取，因为3-0>2，两个元素之间间隔超过2了
    public int ConstrainedSubsetSum(int[] nums, int k) {
        PriorityQueue<int[],int[]> heap = new(Comparer<int[]>.Create((x, y) => y[0]-x[0])); //从大到小排序。这个heap同样也是dp数组（虽然说dp不止数组的记忆形式，但是我习惯了）
        //dp[i]表示从索引0到i处prefix的最大和
        heap.Enqueue(new int[] {nums[0], 0},new int[] {nums[0], 0}); //base case。0是这个数字的索引，用于管理sliding window
        int ans = nums[0];
        for (int i = 1; i < nums.Length; i++) {
            while (i - heap.Peek()[1] > k) { //将k的定义转换一下，就是管理一个长度为k的window。若元素在k之外，将其排除
                heap.Dequeue();
            }
            //heap.Peek()[0]是window内最大的元素。有可能是负数，所以如果是负数的话，不如不拿，加个0完事。这里有点Kadane's algorithm的味道，例题 https://github.com/C0nstellati0n/NoobCTF/blob/main/Leetcode/Hard/Substring%20With%20Largest%20Variance.md
            int curr = Math.Max(0, heap.Peek()[0]) + nums[i];
            ans = Math.Max(ans, curr);
            heap.Enqueue(new int[] {curr, i},new int[] {curr, i});
        }
        return ans;
    }
}
```
Approach 2是将heap换成treemap（红黑树），这样就从heap的O(log n)变成了treemap的O(log k)。Approach 3是个比较新的玩意
```c#
//采样区，但是和editorial的Approach 3想法不谋而合。空间还更好一点
public class Solution {
    public int ConstrainedSubsetSum(int[] nums, int k) {
        //editorial里java用的是Deque<Integer>，应该是双端队列。原来c#的类比是LinkedList
        var deque = new LinkedList<int>(); //deque里存的是索引，方便管理window。同时模拟Monotonic Deque
        int s = 0;
        int e = 1;
        int n = nums.Length;
        deque.AddFirst(0);
        int max = nums[0];
        while(e < n)
        {
            int currMax = Math.Max(nums[e], nums[e] + nums[deque.First.Value]); //因为Monotonic Deque数据结构的性质，第一个值虽然记的是索引，但一定是当前window下最大的数字
            while(deque.Count > 0 && nums[deque.Last.Value] < currMax) //Monotonic Deque的构成。currMax是要新添加的元素，若deque.Last.Value小于它，就破坏了Monotonic的性质，需要移除
            {
                //不用担心移除元素后不够window大小。因为window内已经有比它们大的元素了，后面也轮不到它们
                deque.RemoveLast();
            }
            nums[e] = currMax; //这里应该是直接把nums当作dp数组用，节省空间
            deque.AddLast(e);
            max = Math.Max(max, currMax);
            e++; //e是当前索引
            if(e <= k) //e小于等于k时不用担心window过长
            {
                continue;
            }
            if(deque.First.Value == s)
            {
                deque.RemoveFirst(); //保持window长度不大于k
            }
            s++;
        }
        return max;
    }
}
```