# Minimum Penalty for a Shop

[题目](https://leetcode.com/problems/minimum-penalty-for-a-shop/description/)

提示看完了就懂了。
```c#
public class Solution {
    public int BestClosingTime(string customers) {
        var ans=(Index:-1,Penalty:Int64.MaxValue);
        int yCount=0;
        int nCount=0;
        int penalty=Int32.MaxValue;
        foreach(int cus in customers){
            if(cus=='Y'){
                yCount++;
            }
        }
        int i;
        for(i=0;i<customers.Length;i++){
            penalty=yCount+nCount;
            if(penalty<ans.Penalty){
                ans=(Index:i,Penalty:penalty);
            }
            if(customers[i]=='N'){
                nCount++;
            }
            else{
                yCount--;
            }
        }
        penalty=yCount+nCount;
        if(penalty<ans.Penalty){
            ans=(Index:i,Penalty:penalty);
        }
        return ans.Index;
    }
}
```
```
Runtime
57 ms
Beats
100%
Memory
41.7 MB
Beats
89.47%
```
我这种方法遍历了customers两次，[editorial](https://leetcode.com/problems/minimum-penalty-for-a-shop/editorial/)还有一种只遍历一次的做法。主要是我第一次遍历是为了找Y的数量，从而算出真正的penalty然后找最小的。但仔细想想，这题又不是叫你找最少的penalty的值，而是会造成最小penalty的index。所以我们只遍历一次，遇见Y就penalty-1，遇见N就加1。最后算出来的penalty是实际penalty往下移了几格，不影响相对的差值，最小的还是最小的。