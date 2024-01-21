# [Sum of Subarray Minimums](https://leetcode.com/problems/sum-of-subarray-minimums)

monotonic stack概念难度： 20%

要用monotonic stack的题目难度：80%

发现monotonic stack在题目中的正确用法难度： 150%

采样区做法理解难度：1000000%

solution区个人觉得解释得很好的帖子： https://leetcode.com/problems/sum-of-subarray-minimums/solutions/178876/stack-solution-with-very-detailed-explanation-step-by-step 。但不知道为什么里面的解法现在用会造成溢出，于是我找了类似思路的另一个solution： https://leetcode.com/problems/sum-of-subarray-minimums/solutions/4595335/beats-100-c-java-python-js-explained-with-video-monotonic-stack 。比对了一下，看来是少了`static_cast<ll>`。结果采样区剑走偏锋，出现了这个怪物做法：
```c++
class Solution {
public:
    int mod=1e9+7;
    int sumSubarrayMins(vector<int>& a) {
        int stackSum=a.front(),ans=a.front();
        stack<pair<int,int>> st;
        st.push({a.front(),1});
        for(int i=1;i<a.size();i++){
            pair<int,int> p={a[i],1};
            while(!st.empty() && st.top().first>=a[i]){
                auto [x,y]=st.top();
                stackSum-=x*y;
                p.second+=y;
                st.pop();
            }
            stackSum+=p.first*p.second;
            ans=(ans+0LL+stackSum)%mod;
            st.push(p);
        }
        return ans;
    }
};
```
我就不瞎解释了。不过我发现个规律，[Maximum Score of a Good Subarray](../Hard/Maximum%20Score%20of%20a%20Good%20Subarray.md)也有一种monotonic stack做法，两个做法不谋而合地都有个left数组和right数组，记录当前元素相对数组中其他元素的某种性质。虽然就见了这么两道题，但是大胆猜测：subsequence常用dp，subarray常用monotonic stack，而且这个monotonic stack用来记subarray的索引