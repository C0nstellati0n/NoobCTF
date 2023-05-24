# Maximum Subsequence Score

[题目](https://leetcode.com/problems/maximum-subsequence-score/description/)

题目都叫“Subsequence”了，你告诉我这题和dp一点关系都没有？

```c#
//https://leetcode.com/problems/maximum-subsequence-score/solutions/3082106/java-c-python-priority-queue/
public class Solution {
    public long MaxScore(int[] nums1, int[] nums2, int k) {
        int n = nums1.Length;
        int[][] ess = new int[n][];
        for (int i = 0; i < n; ++i)
            ess[i] = new int[] {nums2[i], nums1[i]}; //把nums1和nums2联系起来
        Array.Sort(ess, (a, b) => b[0] - a[0]); //根据nums2的值降序排序。分组排序是为了让nums1和nums2的数字的索引对应起来，这样排序就会不会打乱它们的索引了。降序是因为题目要求找出索引中最小的数。后面的逻辑不断在往队列里加数，最开始肯定是不足k个数的。那么降序就能保证数字足够k个时对应的nums2中的数字也是min会获取到的数字
        PriorityQueue<int,int> pq = new(Comparer<int>.Create((x, y) => x-y)); //升序排序，毕竟题目说的越大越好
        long res = 0, sumS = 0;
        foreach(int[] es in ess) {
            pq.Enqueue(es[1],es[1]);//将nums1入队列
            sumS = (sumS + es[1]); //按照题目要求计算和
            if (pq.Count > k) sumS -= pq.Dequeue(); //只要k个数，所以把当前队列里最小的数弹出去，并且总和减去弹出的数
            if (pq.Count == k) res = Math.Max(res, (sumS * es[0])); //如果队列里有了k个数，就乘上nums2里的数。取最大值。
        }
        return res;
    }
}
```
```
Runtime
326 ms
Beats
63.64%
Memory
56.1 MB
Beats
63.64%
```

然后是优化版本。
```c#
//https://leetcode.com/problems/maximum-subsequence-score/solutions/3092528/easiest-to-understand/
public class Solution {
    public long MaxScore(int[] a, int[] b, int k) {
        int n = a.Length;
        Tuple<int,int>[] pairs = new Tuple<int,int>[n];
        int i=0;
        for (; i < n; ++i) pairs[i] = new Tuple<int,int>(a[i], b[i]);
        Array.Sort(pairs, (x, y) => y.Item2 - x.Item2);
        PriorityQueue<int,int> q = new(k+1);
        long res = 0, sum = 0;

        i = 0;
        for (; i < k; i++) {
            int x = pairs[i].Item1;
            sum += x;
            q.Enqueue(x,x);
        }
        res = Math.Max(res, sum * pairs[i-1].Item2);

        for (; i < n; i++) {
            q.Enqueue(pairs[i].Item1,pairs[i].Item1);
            sum += pairs[i].Item1;
            sum -= q.Dequeue();
            res = Math.Max(res, sum * pairs[i].Item2);
        }
        return res;
    }
}
```
```
Runtime
319 ms
Beats
90.91%
Memory
57.9 MB
Beats
45.45%
```