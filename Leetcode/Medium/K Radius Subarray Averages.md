# K Radius Subarray Averages

[题目](https://leetcode.com/problems/k-radius-subarray-averages/description/)

我看出来sliding window了，结果最后写的解法还是prefix sum。没办法，hint说用prefix sum我能不用吗？
```c#
public class Solution {
    public int[] GetAverages(int[] nums, int k) {
        if(k==0){
            return nums;
        }
        int n=nums.Length;
        int[] res=new int[n];
        if(n<=2*k){
            Array.Fill(res,-1);
            return res;
        }
        long[] prefixSum=new long[n];
        prefixSum[0]=nums[0];
        for(int i=1;i<n;i++){
            prefixSum[i]=nums[i]+prefixSum[i-1];
        }
        for(int i=0;i<n;i++){
            if(i-k<0||i+k>=n){
                res[i]=-1;
            }
            else if(i-k==0){
                res[i]=(int)(prefixSum[i+k]/(long)(2*k+1));
            }
            else{
                res[i]=(int)((prefixSum[i+k]-prefixSum[i-k-1])/(long)(2*k+1));
            }
        }
        return res;
    }
}
```
```
Runtime
402 ms
Beats
96.72%
Memory
66.4 MB
Beats
6.56%
```
其实不用sliding window是因为我忘了怎么用了……没关系，这不正好复习吗？
```c#
//https://leetcode.com/problems/k-radius-subarray-averages/solutions/1599973/python-3-sliding-window-illustration-with-picture/
public class Solution {
    public int[] GetAverages(int[] nums, int k) {
        int[] res = new int[nums.Length];
        Array.Fill(res,-1);
        int left = 0;
        long curWindowSum=0;
        long diameter=2*k+1;
        for(int right=0;right<nums.Length;right++){
            curWindowSum += nums[right];
            if (right-left+1 >= diameter){
                res[left+k] = (int)(curWindowSum/diameter);
                curWindowSum -= nums[left];
                left += 1;
            }
        }
        return res;
    }
}
```
```
Runtime
395 ms
Beats
100%
Memory
60.7 MB
Beats
85.25%
```