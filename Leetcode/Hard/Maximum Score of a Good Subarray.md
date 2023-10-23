# [Maximum Score of a Good Subarray](https://leetcode.com/problems/maximum-score-of-a-good-subarray)

我似乎明白了leetcode的良苦用心。这个hard一点也不hard啊！
```c#
//discussion区看 Finesse 的评论就懂了
public class Solution {
    public int MaximumScore(int[] nums, int k) {
        int i=k;
        int j=k;
        int left;
        int right;
        int score=nums[k];
        int min=score;
        while(true){
            if(i<=0&&j>=nums.Length-1) break;
            if(i>0) left=nums[i-1];
            else left=-1;
            if(j<nums.Length-1) right=nums[j+1];
            else right=-1;
            if(left>=right){ //记得包含=的情况，不然TLE
                i--;
                min=Math.Min(min,nums[i]);
            }
            else if(right>=left){ //或者这里直接用else。对啊为什么我要用else if？
                j++;
                min=Math.Min(min,nums[j]);
            }
            score=Math.Max((j-i+1)*min,score);
        }
        return score;
    }
}
```
[editorial](https://leetcode.com/problems/maximum-score-of-a-good-subarray/editorial)还有binary search和Monotonic Stack解法。没必要，真的没必要