# The K Weakest Rows in a Matrix

[题目](https://leetcode.com/problems/the-k-weakest-rows-in-a-matrix)

又名“一个写错的符号是怎么逼疯我的”
```c#
public class Solution {
    public int[] KWeakestRows(int[][] mat, int k) {
        int m=mat.Length;
        int n=mat[0].Length;
        int[] ans=new int[k];
        PriorityQueue<int,Tuple<int,int>> maxHeap = new(Comparer<Tuple<int,int>>.Create((x, y) => x.Item1!=y.Item1?x.Item1-y.Item1:x.Item2-y.Item2));
        for(int i=0;i<m;i++){
            int count=0;
            for(int j=0;j<n;j++){
                if(mat[i][j]==1){
                    count++;
                }
            }
            maxHeap.Enqueue(i,new Tuple<int,int>(count, i));
        }
        for(int i=0;i<k;i++){
            ans[i]=maxHeap.Dequeue();
        }
        return ans;
    }
}
```
```
Runtime
124 ms
Beats
100%
Memory
46.3 MB
Beats
74.12%
```
最开始`x.Item1!=y.Item1`写成`x.Item1==y.Item1`了，陷入长达十几分钟的自我怀疑（不是吧这个bug找这么久？）。没关系最后出来了就好。其它做法：
- https://leetcode.com/problems/the-k-weakest-rows-in-a-matrix/solutions/1201679/c-python3-no-heap-no-bs-simple-sort-99-20 ：不用heap而是变化过的sort
- https://leetcode.com/problems/the-k-weakest-rows-in-a-matrix/solutions/496555/java-best-solution-100-time-space-binary-search-heap ：思路和我这个差不多，不过计算1的数量时使用binary search