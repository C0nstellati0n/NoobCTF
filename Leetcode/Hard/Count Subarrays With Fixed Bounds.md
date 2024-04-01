# [Count Subarrays With Fixed Bounds](https://leetcode.com/problems/count-subarrays-with-fixed-bounds)

回旋镖这么快就打过来了？
```c++
//https://leetcode.com/problems/count-subarrays-with-fixed-bounds/solutions/2708099/java-c-python-sliding-window-with-explanation
class Solution {
public:
    long long countSubarrays(vector<int>& A, int minK, int maxK) {
        long res = 0, jbad = -1, jmin = -1, jmax = -1, n = A.size();
        for (int i = 0; i < n; ++i) {
            if (A[i] < minK || A[i] > maxK) jbad = i;
            if (A[i] == minK) jmin = i;
            if (A[i] == maxK) jmax = i;
            res += max(0L, min(jmin, jmax) - jbad);
        }
        return res;
    }
};
```
[昨天](./Subarrays%20with%20K%20Different%20Integers.md)刚说已经看完全部sliding window变种了，今天就来了个条件是between的题。看提示说什么“Think of the inclusion-exclusion principle”，我就以为要跟昨天一样调用两次。还是lee佬强，不仅思路清晰，写解析也很牛逼

所以我们遍历A数组一遍，目前subarray的结尾index是i。如果目前还没有出现过等于minK或maxK的元素或是只出现一个，res会加0，没问题。那假设jmin小于jmax等于i，有多少subarray满足between的条件？答案取决于jbad，即那个不在minK到maxK之间的元素。如果jbad小于jmin，subarray的数量就等于jmin-jbad，因为从jmin-jbad到jmin这中间的任意元素开始，到i，都是合法的subarray。此时如果maxK不动，i加上1，subarray的数量还是等于jmin-jbad，即那些从jmin-jbad到jmin这中间的任意元素开始到i+1的所有subarray

如果jbad在jamx和jmin中间，从代码里也能看出，不会有任何subarray。一个jbad把jmin和jmax割开，无法形成好的subarray。如果jbad大于jmin和jmax，此时应该有subarray啊，但是代码加的数量还是0，为啥？因为这之前肯定已经计数过这些subarray了

把jmin和jmax出现的索引调换不会影响结果