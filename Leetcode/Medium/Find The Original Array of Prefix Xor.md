# [Find The Original Array of Prefix Xor](https://leetcode.com/problems/find-the-original-array-of-prefix-xor)

好简单的medium
```c#
public class Solution {
    public int[] FindArray(int[] pref) {
        int curr=pref[0];
        int[] ans=new int[pref.Length];
        ans[0]=curr;
        int copy=curr;
        for(int i=1;i<pref.Length;i++){
            curr=copy;
            curr^=pref[i];
            ans[i]=curr;
            copy^=curr;
        }
        return ans;
    }
}
```
但是等一下。有没有一种多此一举的感觉？有就对了。因为pref[i]和pref[i-1]就差了一个xor的数字，正好这个数字就是我们要找的，那么直接xor两者就能得到，完全不需要额外的什么curr和copy
```c#
//https://leetcode.com/problems/find-the-original-array-of-prefix-xor/editorial
class Solution {
    public int[] FindArray(int[] pref) {
        int n = pref.Length;
        for (int i = n - 1; i > 0; i--) {
            pref[i] = pref[i] ^ pref[i - 1];
        }
        return pref;
    }
}
```