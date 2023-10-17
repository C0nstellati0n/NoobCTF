# [Pascal's Triangle II](https://leetcode.com/problems/pascals-triangle-ii)

啊？c#里array算`IList<int>`啊?
```c#
public class Solution {
    public IList<int> GetRow(int rowIndex) {
        int[,] triangle = new int[rowIndex+1,rowIndex+1];
        List<int> res=new();
        for (int i = 0; i < rowIndex+1; i++) {
            triangle[i,0] = triangle[i,i] = 1;
        }
        for (int i = 2; i < rowIndex+1; i++) {
            for (int j = 1; j < i; j++) {
                triangle[i,j] = triangle[i - 1,j] + triangle[i - 1,j - 1];
            }
        }
        for(int j=0;j<rowIndex+1;j++){
            res.Add(triangle[rowIndex,j]);
        }
        return res;
    }
}
```
```
Runtime
80 ms
Beats
87.86%
Memory
36.1 MB
Beats
37.54%
```
此答案完全抄之前做过的一道前置题：[Pascal's Triangle](./Pascal's%20Triangle.md).然后照例去看看大佬们的答案。
```c#
//https://leetcode.com/problems/pascals-triangle-ii/solutions/38420/here-is-my-brief-o-k-solution
public class Solution { 
    public IList<int> GetRow(int rowIndex) 
    { 
        int[] A=new int[rowIndex+1]; 
        A[0] = 1; 
        for(int i=1; i<rowIndex+1; i++) 
            for(int j=i; j>=1; j--) A[j] += A[j-1]; 
        return A; 
    } 
ß}
```
```
Runtime 78 ms 
Beats 92.56% 
Memory 36.1 MB 
Beats 37.54%
```
好，就在我将这个答案从c++改成c#时，我将vector改成了int[]，然后return那里啥也没动就返回了。提交后发现没问题，然后突然发觉：“我刚刚返回了个什么？” 之前的我一直以为`IList<int>`只接受`List<int>`，原来int array也行啊？

最后是喜闻乐见的数学解法：
```c#
//https://leetcode.com/problems/pascals-triangle-ii/solutions/1203260/very-easy-o-n-time-0-ms-beats-100-simple-maths-all-languages
public class Solution {
    public IList<int> GetRow(int r) {
        var ans = new int[r+1];
        ans[0]=ans[r]=1;
        long temp=1;
        for(int i=1,up=r;i<r;i++,up--){
            temp = temp * up / i;
            ans[i]=(int)temp;
        }
        return ans;
    }
}
```
```
Runtime
83 ms
Beats
76.38%
Memory
36.1 MB
Beats
58.74%
```