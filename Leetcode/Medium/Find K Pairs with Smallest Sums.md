# Find K Pairs with Smallest Sums

[题目](https://leetcode.com/problems/find-k-pairs-with-smallest-sums/description/)

这题的80%都很好理解，不过剩下的20%足够让我懵逼了。
```c#
//https://leetcode.com/problems/find-k-pairs-with-smallest-sums/solutions/84551/simple-java-o-klogk-solution-with-explanation/
//类似做法1： https://leetcode.com/problems/find-k-pairs-with-smallest-sums/solutions/209985/python-heap-solution-with-detail-explanation/
//类似做法2: https://leetcode.com/problems/find-k-pairs-with-smallest-sums/solutions/84566/share-my-solution-which-beat-96-42/
public class Solution {
    public IList<IList<int>> KSmallestPairs(int[] nums1, int[] nums2, int k) {
        PriorityQueue<int[],int[]> que = new(Comparer<int[]>.Create((a,b)=>a[0]+a[1]-b[0]-b[1]));
        List<IList<int>> res = new();
        for(int i=0; i<nums1.Length && i<k; i++) que.Enqueue(new int[]{nums1[i], nums2[0], 0},new int[]{nums1[i], nums2[0], 0});
        while(k-- > 0 && que.Count!=0){
            int[] cur = que.Dequeue();
            res.Add(new List<int>{cur[0], cur[1]});
            if(cur[2] == nums2.Length-1) continue;
            que.Enqueue(new int[]{cur[0],nums2[cur[2]+1], cur[2]+1},new int[]{cur[0],nums2[cur[2]+1], cur[2]+1});
        }
        return res;
    }
}
```
```
Runtime
369 ms
Beats
85.88%
Memory
65.7 MB
Beats
11.76%
```
用堆这一点已经在discussion看到了，所以难点在哪里？难点在于，怎么确定当前pair就是最小的？乍一听是句废话，都用minHeap了还担心这个？问题在于，不能保证当前最小的pair已经在heap里了。无脑做法是爆破，把所有可能的pair全放进去，好直接TLE。所以要找到一种放法，保证放入heap的pair递增排序。那这个应该简单啊，两个数组都是排序好的，一点一点往下推不就行了？用nums1最小的配上nums2里最小的然后nums2不断往下似乎可行，然而题目并没有保证数字不会重复，万一nums1里第二个和第一个一样小呢？那第二小的不就变成nums[0]+nums2[0]了吗？还有很多种复杂的情况，全考虑进去不仅效率低，还很容易错。

所以第一个解法就先把所有nums1与nums2可能的配对全放进heap，然后再慢慢加nums2的索引。啊就这么简单，多少复杂的情况全部通吃。类似做法1没有提前得那个for循环，而是一次尝试enqueue两对（nums1索引+1或者nums2索引+1），同样解决了上面提到的问题。类似做法2则是反过来，将nums2的配对全放进去，然后增加nums1索引。