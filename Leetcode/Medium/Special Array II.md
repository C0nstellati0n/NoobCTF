# [Special Array II](https://leetcode.com/problems/special-array-ii)

以前：不是为什么要修改input啊？为了省这么点内存至于吗？

现在：至于
```c++
class Solution {
public:
    vector<bool> isArraySpecial(vector<int>& nums, vector<vector<int>>& queries) {
        int n=nums.size();
        int curEnd=n-1;
        bool even=nums.back()%2==0;
        for(int i=n-1;i>-1;i--){
            if((nums[i]%2==0)==even) nums[i]=curEnd;
            else{
                curEnd=i;
                even=nums[i]%2==0;
                nums[i]=i;
            }
            even=!even;
        }
        vector<bool> res;
        res.reserve(n);
        for(const auto& query:queries){
            res.push_back(nums[query[0]]>=query[1]);
        }
        return res;
    }
};
```
看了一圈，感觉比较契合editorial的`Approach 3: Sliding Window`。但是受[昨天的题目](./Two%20Best%20Non-Overlapping%20Events.md)影响，我的脑回路和其他人不一样，喜欢倒着来

玩了这么久leetcode终于稍微聪明了几回