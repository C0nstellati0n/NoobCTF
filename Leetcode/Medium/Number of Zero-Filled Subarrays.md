# Number of Zero-Filled Subarrays

[题目](https://leetcode.com/problems/number-of-zero-filled-subarrays/description/)

随手一写就写出来了速度世界最慢的算法。

```c#
public class Solution {
    public long ZeroFilledSubarray(int[] nums) {
        long total=0;
        int j;
        for(int i=0;i<nums.Length;i++){
            if(nums[i]==0){
                j=i;
                while(nums[j]==0){
                    total++;
                    j++;
                    if(j>=nums.Length){
                        break;
                    }
                }
            }
        }
        return total;
    }    
}
```

没有数据。因为慢到触发`Time Limit Exceeded`。不过思路没有走得太偏，改一下就好了。

```c#
//https://leetcode.com/problems/number-of-zero-filled-subarrays/solutions/3321976/java-c-simple-solution-easy-to-understand/
public class Solution {
    public long ZeroFilledSubarray(int[] nums) {
        long total=0;
        long current=0;
        for(int i=0;i<nums.Length;i++){
            if(nums[i]==0){
                current++;
                total+=current;
            }
            else{
                current=0;
            }
        }
        return total;
    }    
}
```

```
Runtime
274 ms
Beats
64.71%
Memory
54 MB
Beats
5.88%
```

如果再认真一点，发现计算子数组的公式后，速度就会再上升一个层次。

```c#
//https://leetcode.com/problems/number-of-zero-filled-subarrays/solutions/3322097/linear-traversal-c-and-java-solution/
class Solution {
    public long ZeroFilledSubarray(int[] nums) {
        long res = 0;
        long counter = 0;
        foreach(int ele in nums){
            if(ele==0){
                counter++;
            }else{
                res += (counter*(counter+1))/2;
                counter = 0;
            }
        }
        if(counter!=0){
            res += (counter*(counter+1))/2;
        }
        return res;
    }
}
```

```
Runtime
258 ms
Beats
100%
Memory
53.3 MB
Beats
5.88%
```