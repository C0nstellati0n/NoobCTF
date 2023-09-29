# Sort Array By Parity

[题目](https://leetcode.com/problems/sort-array-by-parity)

我需要easy来重建自信心。
```c#
public class Solution {
    public int[] SortArrayByParity(int[] nums) {
        List<int> ans=new();
        foreach(int num in nums){
            if((num&1)==0){
                ans.Insert(0,num);
            }
            else{
                ans.Add(num);
            }
        }
        return ans.ToArray();
    }
}
```
```
Runtime
119 ms
Beats
99.48%
Memory
47.2 MB
Beats
12.24%
```
内存不太行，毕竟用了一个list。但有一个神奇的方法，去看memory采样区最佳，只要在最后加上一句`GC.Collect();`，内存瞬间冲100%，甚至比O(1)做法的内存还好。代价是Runtime变成了最差。
```c#
//https://leetcode.com/problems/sort-array-by-parity/solutions/170734/c-java-in-place-swap/
public class Solution {
    public int[] SortArrayByParity(int[] A) {
        for (int i = 0, j = 0; j < A.Length; j++)
            if ((A[j]&1) == 0) {
                (A[i],A[j])=(A[j],A[i]); //赞美tuple！
                i++;
            }
        return A;
    }
}
```
```
Runtime
114 ms
Beats
100%
Memory
47 MB
Beats
34.11%
```