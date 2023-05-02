# Sign of the Product of an Array

[题目](https://leetcode.com/problems/sign-of-the-product-of-an-array/description/)

5分钟写不出来解都对不起easy的标签。

```c#
public class Solution {
    public int ArraySign(int[] nums) {
        if(nums.Contains(0)){
            return 0;
        }
        int res=1;
        foreach(int num in nums){
            if(num<0){
                res*=-1;
            }
            else{
                res*=1;
            }
        }
        return res;
    }
}
```

```
Runtime
91 ms
Beats
50.95%
Memory
39.7 MB
Beats
26.62%
```

但是这个解法不注重细节。开头Contains没必要，而且也不用乘-1,计算负数的数量就好了。

```c#
//https://leetcode.com/problems/sign-of-the-product-of-an-array/solutions/3476080/c-easy-approach-explained/
public class Solution {
    public int ArraySign(int[] nums) {
        int cnt = 0;
        foreach(int i in nums) 
        {
            if(i == 0) return 0;
            if(i < 0) cnt++;
        }
        return cnt%2==1 ? -1 : 1;
    }
}
```

```
Runtime
86 ms
Beats
74.14%
Memory
39.4 MB
Beats
57.41%
```