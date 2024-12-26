# [Target Sum](https://leetcode.com/problems/target-sum)

dp再次从一堆知识点中跳出来准确杀死我:(
```c++
//改编自采样区
//类似editorial的 Approach 3: 2D Dynamic Programming
class Solution {
public:
    int findTargetSumWays(vector<int>& nums, int target) {
      int n = nums.size();
      int sum = accumulate(nums.begin(),nums.end(),0);
      //这块的推导见discussion区lingarajbal的评论
      if((sum+target)%2!=0) return 0;
      if(abs(target)>abs(sum)) return 0;
      int new_target = (sum+target)/2; //现在要找sum为new_target的subset数量。差点把subset跟subarray搞混了，subset类似subsequence但可以有空集
      vector<vector<int>> t(n+1,vector<int>(new_target+1)); //dp[i][j]定义为前i个元素组合出的subsets的sum为j的数量
      t[0][0] = 1; //base case
      for(int i =1 ;i<n+1; i++){
         for(int j = 0; j<new_target+1;j++){ //要算前i个元素可组成sum的所有可能性
            if(nums[i-1]<=j){ //这里我是这样理解的，因为dp定义的是前i个元素而不是索引，所以这里要考虑的是nums[i-1]而不是nums[i]。感觉还是从dp定义来理解dp公式比较简单
                t[i][j] = t[i-1][j-nums[i-1]] + t[i-1][j];
                //如果之前能组成j-nums[i-1]，就能把另一条路的数量也加上
            }
            else{
                //上一行就已经有t[i-1][j]个subset了，再多一个数所形成的subset数量不会比这个更少
                t[i][j] = t[i-1][j];
            }
         }
      }
      return t[n][new_target];
    }
};
```