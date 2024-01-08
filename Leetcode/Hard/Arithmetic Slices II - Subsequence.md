# [Arithmetic Slices II - Subsequence](https://leetcode.com/problems/arithmetic-slices-ii-subsequence)

感觉这辈子只能是个懒惰的笨蛋了
```c++
//采样区
// https://leetcode.com/problems/arithmetic-slices-ii-subsequence/solutions/849944/c-with-picture-base-optimizations 有解析
using ll = long;
const uint max_n = 1000;
uint dp[max_n][max_n]; //dp[i][j]: number of the arithmetic subsequence ending at i, with the difference a[i] - a[j]
class Solution {
public:
    int numberOfArithmeticSlices(vector<int>& a) {
        uint n = a.size();
        uint res = 0;
        unordered_map<int, vector<uint>> ai = {}; //记每个元素出现的索引。至于为什么值类型是vector<uint>，因为同一个元素可能在不同位置出现多次
        for (uint i = 0; i < n; i++) ai[a[i]].push_back(i);
        for (uint i = 1; i < n; i++) {
            for (uint j = 0; j < i; j++) {
                dp[i][j] = 0;
                auto p = 2l * a[j] - a[i]; //获取当前Arithmetic Subsequence的前一个元素。见评论区 wulouis0511 的评论
                if (p < INT_MIN || p > INT_MAX)
                    continue;
                auto ii = ai.find(p); //检查数组里是否有这个元素
                if (ii != ai.end()) {
                    for (auto k : ai[p]) { //要是有的话，遍历该元素出现的所有索引
                        if (k >= j) //k为前一个元素的索引，j代表当前元素的索引。前一个元素的索引自然不能超过当前元素的索引，不然就不是Subsequence了
                            break;
                        dp[i][j] += dp[j][k] + 1;
                    }
                }
                res += dp[i][j]; //关于此处如何确定dp[i][j]的subsequence长度大于等于3，个人猜想：因为最开始算Arithmetic Subsequence的前一个元素时，用了a[j]-a[i]获取差值，此处已经有2个元素；加上前一个元素，至少有3个，故可以直接加
            }
        }
        return res;
    }
};
```
虽然时间复杂度还是 $n^2$ ，但是会比普通的做法快上不少。据大佬所说，秘诀就在于提前找了那个“Arithmetic Subsequence的前一个元素”。另外在看Base Solution时，注意到unordered_map最好检查键是否存在，不然加内存和用时