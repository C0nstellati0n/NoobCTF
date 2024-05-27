# [Student Attendance Record II](https://leetcode.com/problems/student-attendance-record-ii)

我真get不到dp。其实相似思路我之前见过，但是我太垃圾了
```c++
// https://leetcode.com/problems/student-attendance-record-ii/editorial 第一种解法
//个人觉得是最容易理解的做法
//神奇的地方在于，editorial里最好的做法也就1000ms左右，但是采样区第一0ms……看了一眼那个算法实现，一看就是经常打算法竞赛的
class Solution {
    int MOD = 1000000007;
    // Cache to store sub-problem results.
    vector<vector<vector<int>>> memo;
public:
    // Recursive function to return the count of combinations of length 'n' eligible for the award.
    int eligibleCombinations(int n, int totalAbsences, int consecutiveLates) {
        // If the combination has become not eligible for the award,
        // then we will not count any combinations that can be made using it.
        if (totalAbsences >= 2 or consecutiveLates >= 3) {
            return 0;
        }
        // If we have generated a combination of length 'n' we will count it.
        if (n == 0) {
            return 1;
        }
        // If we have already seen this sub-problem earlier, we return the stored result.
        if (memo[n][totalAbsences][consecutiveLates] != -1) {
            return memo[n][totalAbsences][consecutiveLates];
        }
        int count = 0;
        // We choose 'P' for the current position.
        count = eligibleCombinations(n - 1, totalAbsences, 0);
        // We choose 'A' for the current position.
        count = (count + eligibleCombinations(n - 1, totalAbsences + 1, 0)) % MOD;
        // We choose 'L' for the current position.
        count = (count + eligibleCombinations(n - 1, totalAbsences, consecutiveLates + 1)) % MOD;
        // Return and store the current sub-problem result in the cache.
        return memo[n][totalAbsences][consecutiveLates] = count;
    }
    int checkRecord(int n) {
        // Initialize the cache.
        memo = vector<vector<vector<int>>>(n + 1, vector<vector<int>>(2, vector<int>(3, -1)));
        // Return count of combinations of length 'n' eligible for the award.
        return eligibleCombinations(n, 0, 0);
    }
};
```