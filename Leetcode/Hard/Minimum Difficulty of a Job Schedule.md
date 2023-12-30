# [Minimum Difficulty of a Job Schedule](https://leetcode.com/problems/minimum-difficulty-of-a-job-schedule)

现在没人能说我抄都抄不明白了
```c++
//取自discussion区shivamaggarwal513的评论，解析得非常好
class Solution {
    int ans_max=1000*300;
public:
    int minDifficulty(vector<int>& jobDifficulty, int d) {
        vector<vector<int>> dp(jobDifficulty.size(),vector<int>(d+1));
        int ans=helper(0,d,dp,jobDifficulty);
        return ans==ans_max?-1:ans;
    }
    int helper(int i,int d,vector<vector<int>>& dp,vector<int>& difficulty){
        if(i==difficulty.size()||d==0){
            if(i==difficulty.size()&&d==0) return 0;
            else return ans_max;
        }
        if(dp[i][d]!=0) return dp[i][d]-1;
        int res=ans_max;
        int dayDifficulty = 0;
        int next=0;
        for(int j=i;j<difficulty.size()-d+1;j++){ //感觉看出点subproblem的门道了。这题考分配job，因为每天至少得有一个job，那么第一天的分割最多只能分到difficulty.size()-d，多了后剩下的就没法做到一天分一个job了
        //于是for循环遍历所有第一天可能的分法，假设分在1，剩下的j+1和d-1构成一个subproblem，开始递归
        //所以目前dp的门道就是dp定义（记忆的dp state代表什么），dp equation（各个dp state之间的关系），subproblem（在哪里递归），base case（何处终止递归）
        //不看优化做法和递归做法了，真整不明白
            dayDifficulty = max(dayDifficulty, difficulty[j]);
            next=helper(j + 1, d - 1,dp,difficulty);
            if(next!=ans_max)
                res=min(res, dayDifficulty + next);
        }
        dp[i][d]=res+1; //关于为什么要存res+1，因为有dp state等于0的情况，假如不存+1就不能在上面写 if(dp[i][d]!=0) 了。存个res+1就能避免这种情况，还不用初始化dp为-1
        return res;
    }
};
```
中间其实出了点问题，但都给我自己搞好了。抄明白哩