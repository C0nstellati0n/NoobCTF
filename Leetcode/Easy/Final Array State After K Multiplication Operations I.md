# [Final Array State After K Multiplication Operations I](https://leetcode.com/problems/final-array-state-after-k-multiplication-operations-i)

很简单的一道题，但借此机会学习一下c++的make_heap相关函数。相比于直接创建heap再push n的元素的nlogn复杂度，make_heap的复杂度只有n
```c++
//https://leetcode.com/problems/final-array-state-after-k-multiplication-operations-i/editorial
class Solution {
public:
    vector<int> getFinalState(vector<int>& nums, int k, int multiplier) {
        vector<pair<int, int>> heap;
        for (int i = 0; i < nums.size(); i++) {
            heap.push_back({nums[i], i});
        }
        make_heap(heap.begin(), heap.end(), greater<>());
        while (k--) {
            pop_heap(heap.begin(), heap.end(), greater<>());
            auto [value, i] = heap.back();
            heap.pop_back();
            nums[i] *= multiplier;
            heap.push_back({nums[i], i});
            push_heap(heap.begin(), heap.end(), greater<>());
        }
        return nums;
    }
};
```