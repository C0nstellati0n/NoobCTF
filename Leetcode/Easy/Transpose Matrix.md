# [Transpose Matrix](https://leetcode.com/problems/transpose-matrix)

正如10月的连续hard一样，12月的连续easy也给我带来了极大的震撼
```c++
class Solution {
public:
    vector<vector<int>> transpose(vector<vector<int>>& matrix) {
        //https://stackoverflow.com/questions/17663186/initializing-a-two-dimensional-stdvector
        vector<vector<int>> ans(matrix[0].size(),vector<int>(matrix.size()));
        for(int i=0;i<matrix.size();i++){
            for(int j=0;j<matrix[i].size();j++){
                ans[j][i]=matrix[i][j];
            }
        }
        return ans;
    }
};
```