# [Sum of All Subset XOR Totals](https://leetcode.com/problems/sum-of-all-subset-xor-totals)

布响丸啦！到最后连easy都不会写啊！
```c++
//https://leetcode.com/problems/sum-of-all-subset-xor-totals/editorial 的第二种解法
//第一种解法先用backtrack生成了所有的subset，然后遍历subset求和。第二种做法其实已经涵盖第一种了
//第三种是天才的做法
class Solution {
public:
    int subsetXORSum(vector<int>& nums) {
        return XORSum(nums, 0, 0); 
    }
private:
    int XORSum(vector<int>& nums, int index, int currentXOR) {
        // Return currentXOR when all elements in nums are already considered
        if (index == nums.size()) return currentXOR;
        // Calculate sum of subset xor with current element
        int withElement = XORSum(nums, index + 1, currentXOR ^ nums[index]);
        // Calculate sum of subset xor without current element
        int withoutElement = XORSum(nums, index + 1, currentXOR);
        // Return sum of xor totals
        return withElement + withoutElement;
    }
};
```
你真叫我看我也是能看懂的。呃，我搞混backtrack和bitmask了。我一直想着怎么生成全部的subset。但看大家提到bitmask，联想之前做过的几道题，疯狂思考怎么用bitmask生成subset。我要真这么想也没问题，但我竟然想着拿递归+backtrack配合bitmask生成subset（感觉有点押韵）。等于我把几种可能的解法全部混在一起了。我到底在想什么啊？

心心念念的bitmask解法如下：
```c++
//https://leetcode.com/problems/sum-of-all-subset-xor-totals/solutions/1211182/one-liner-bitmask
//一直想不出来怎么用bitmask表示出全部的subset。结果这样看来遍历所有小于 1 << nums.size() 的数字就行了？
class Solution {
public:
    int subsetXORSum(vector<int>& nums) {
        int res = 0;
        for (auto i = 1; i < (1 << nums.size()); ++i) { //i是全部可能的subset
            int total = 0;
            for (auto j = 0; j < nums.size(); ++j) //j取出subset对应的数字
                if (i & (1 << j))
                    total ^= nums[j];
            res += total;
        }
        return res;
    }
};
```