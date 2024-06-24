# [Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit](https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit)

认识了一个之前没听过的数据结构——multiset。可理解成排序的set，但可以有重复的元素。相比priority_queue，用multiset可以同时获取最大和最小的元素，无需定义两个heap，一个max heap，一个min heap
```c++
class Solution {
public:
    int longestSubarray(vector<int>& nums, int limit) {
        int left=0;
        //默认按从小到大的顺序排序
        multiset<int> vals;
        int ans=0;
        for(int right=0;right<nums.size();right++){
            vals.insert(nums[right]);
            //注意末尾的元素是rbegin不是end。end似乎是理论最小的元素，不一定在multiset里（比如我明明只往里面放了个4，end出来的结果是1）
            while(*vals.rbegin()-*vals.begin()>limit){
                vals.erase(vals.find(nums[left]));
                left++;
            }
            ans=max(ans,right-left+1);
        }
        return ans;
    }
};
```
但是multiset添加、删除、查找的操作都是log(n)复杂度。这时不如用两个deque，deque在两边添加、删除元素的操作复杂度都是n
```c++
//采样区
class Solution {
public:
    int longestSubarray(vector<int>& nums, int limit) {
        // if the diff between the max and min element of an subarray < k then all other 
        // elements' diff is also < k
        int n = nums.size();
        if(nums.size()==0)return 0;
        // we will keep queue to track the index of max and min element in current window 
        // q1 will track max and subsequent index value will decrease 
        // q2 will track min and subsequent index value will increase 
        deque<int>q1,q2;   
        int i=0,j=0,ans=0;
        while(j<n){
            // to maintain order - if new element is greater than last element 
            // remove last and insert current element in q1  vice versa for q2
            while(!q1.empty() && nums[q1.back()]<nums[j])q1.pop_back();
            while(!q2.empty() && nums[q2.back()]>nums[j])q2.pop_back();
            q1.push_back(j);
            q2.push_back(j);
            while(!q1.empty() && !q2.empty() &&
             (nums[q1.front()] - nums[j]>limit || nums[j]-nums[q2.front()]>limit)){
                if(nums[q1.front()] - nums[j]>limit){
                    i= max(i,q1.front()+1);
                    q1.pop_front();
                }
                if(nums[j]-nums[q2.front()]>limit){
                    i= max(i,q2.front()+1);
                    q2.pop_front();
                }
             }
            ans=max(ans,j-i+1);
            j++;
        }
        return ans;
    }
};
```