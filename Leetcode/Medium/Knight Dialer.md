# [Knight Dialer](https://leetcode.com/problems/knight-dialer)

去discussion找了思路，editorial稍微抄了个jumps表（因为可恶的整形溢出）
```c++
//思路来源discussion区 psionl0 的评论
class Solution {
public:
    int knightDialer(int n) {
        int dp[n][10]; //dp[i][j]表示从j号数字跳i步的所有可能数量
        int mod=1e9+7;
        for(int i=0;i<10;i++){
            dp[0][i]=1;
        }
        vector<vector<int>> jumps = { //感谢editorial提供的表
            {4, 6},
            {6, 8},
            {7, 9},
            {4, 8},
            {3, 9, 0},
            {},
            {1, 7, 0},
            {2, 6},
            {1, 3},
            {2, 4}
        };
        int temp;
        for(int i=1;i<n;i++){
            for(int j=0;j<10;j++){
                temp=0;
                for(int jump:jumps[j]){ //最开始我用switch case，根据j的不同加的dp也不同，比如case 4:dp[i][4]=(dp[i-1][3]+dp[i-1][9]+dp[i-1][0])%mod。然后第三个testcase溢出了导致结果很奇怪，百思不得其解后才觉得是不是溢出了啊？
                    temp=(temp+dp[i-1][jump])%mod; //所以这里搞个temp，每加一个就模mod
                }
                dp[i][j]=temp; //这里dp可进行空间优化，因为全程只用了dp[i-1]和dp[i]。参考editorial
            }
        }
        int ans=0;
        for(int i=0;i<10;i++){
            ans=(ans+dp[n-1][i])%mod; //所以最后是n-1则是因为i也算个数字，n要少一位
        }
        return ans;
    }
};
```