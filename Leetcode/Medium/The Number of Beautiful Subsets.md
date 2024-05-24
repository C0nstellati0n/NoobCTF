# [The Number of Beautiful Subsets](https://leetcode.com/problems/the-number-of-beautiful-subsets)

还是稍微看了一眼答案才做出来。差了一行代码
```c++
class Solution {
private:
    int ans=0;
public:
    int beautifulSubsets(vector<int>& nums, int k) {
        //如果提前sort元素，就只用考虑nums[i]-k而不用考虑nums[i]+k了
        //因为要算的是subset，subset本身就是随意取元素，排序改变元素顺序也没事
        sort(nums.begin(),nums.end());
        unordered_map<int,int> cnt;
        dfs(nums,cnt,k,0);
        return ans;
    }
    void dfs(const vector<int>& nums,unordered_map<int,int>& cnt,const int& k,int index){
        if(index>=nums.size()){
            return;
        }
        dfs(nums,cnt,k,index+1); //注意不要漏这句。下面那个if语句考虑拿当前元素的情况，需要检查是否符合题目条件。但是无论当前元素是否符合条件，都可以选择不拿，计算不包含当前元素的subset
        if(!cnt.contains(nums[index]-k)||cnt[nums[index]-k]==0){
            cnt[nums[index]]++;
            dfs(nums,cnt,k,index+1);
            ans++;
            cnt[nums[index]]--;
        }
    }
};
```
第一次写了个bitset遍历解法，太慢了，直接TLE。现在想想应该是少了那个if语句，没有提前修剪掉不符合条件的subset

这是个 $O(2^n)$ 解法。也有 $O(n\space log\space n)$ 解法。非常难。见[editorial](https://leetcode.com/problems/the-number-of-beautiful-subsets/editorial)和 https://leetcode.com/problems/the-number-of-beautiful-subsets/solutions/3363862/c-java-python-evolve-brute-force-to-dp-explained-7-approaches 。猜猜这个解法是什么？dp！哥们你在这蹲我呢？继续佐证我已有的观点：dp是学不会的。dp的精髓就是其transition公式，然而这个公式每道题都不一样，比如像这道题一样难的公式。我还是洗洗睡吧