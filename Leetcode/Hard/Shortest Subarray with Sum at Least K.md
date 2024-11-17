# [Shortest Subarray with Sum at Least K](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k)

我竟然看懂了discussion区 pbalogh 的评论还根据此写出了算法。bro终于有脑子了（
```c++
class Solution {
public:
    int shortestSubarray(vector<int>& nums, int k) {
        vector<long> prefix(nums.size()+1);
        for(int i=1;i<nums.size()+1;i++){
            prefix[i]=prefix[i-1]+nums[i-1]; //prefix[i]: 元素i之前的所有元素之和（不包含元素i）
        }
        deque<int> dq; //一个严格递增的monotonic “stack”
        int ans=nums.size()+1;
        for(int i=0;i<prefix.size();i++){
            //类似sliding window的处理方式
            //处理dq记录的subarray和已经大于等于k的情况
            while(!dq.empty()&&prefix[dq.back()]-prefix[dq.front()]>=k){
                ans=min(ans,dq.back()-dq.front());
                dq.pop_front(); //毕竟当前subarray的和已经满足要求了，后面就算也满足要求，长度也不会比现在更短了。可以放心pop掉
            }
            //拿那个评论的例子。nums [1400, -500, 50, 1490]的prefix为[0, 1400, 900, 950, 2440]
            //很明显我们不需要考虑1400（假设索引是i）。假如prefix[j]-prefix[i]超过k的话，prefix[j]-prefix[i+1]（900）肯定也超过（还是更短的subarray）；即使prefix[j]-prefix[i]不超过k，prefix[j]-prefix[i+1]也有可能超过。无论是哪种情况，都不需要考虑i
            //上述情况只会出现在非单调递增的数组。所以我们维持一个monotonic stack：prefix[j]-prefix[i]满足条件的话，prefix[j]-prefix[i+1]不一定满足条件；prefix[j]-prefix[i]不满足条件的话，prefix[j]-prefix[i+1]一定也不满足条件。一个类sliding window，和上述情况的区别在于，此时i需要被考虑，不是多余的
            while(!dq.empty()&&prefix[dq.back()]>=prefix[i]){
                dq.pop_back();
            }
            dq.push_back(i);
        }
        //有点冗余。真不会设计了，不知道怎么把这段逻辑也放在for循环里
        while(prefix[dq.back()]-prefix[dq.front()]>=k){
            ans=min(ans,dq.back()-dq.front());
            dq.pop_front();
        }
        return ans==nums.size()+1?-1:ans;
    }
};
```
计算prefix和dq和冗余部分其实可以一起放在for循环里。见 https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/solutions/143726/c-java-python-o-n-using-deque 。但代码好像会报错？

deque在这里会拖慢程序。不用deque的同思路做法：
```c++
//采样区
//感觉是算法竞赛选手写的
//神奇语法+无敌算法+莫名其妙的变量命名
const int MAX_N = 100000 + 1;
int* nums;
long long st_s[MAX_N];
int pos[MAX_N];
class Solution {
public:
    int shortestSubarray(vector<int>& _nums, int k) {
        int n = _nums.size();
        nums = &_nums[0];
        long long sp = 0LL; //当前sum
        int res = n + 1;
        //类似sliding window的left和right
        int b = 0, e = 0;
        st_s[e] = 0; //prefix，但同时是monotonic stack
        //不用deque的关键是这个pos数组。e指针负责写入prefix，但由于要保证其同时是monotonic stack，e的值不等于对应元素的索引。所以要额外记录
        pos[e++] = -1;
        for (int i = 0; i < n; i++) {
            sp += nums[i];
            while (b < e && sp - st_s[b] >= k) {
                res = std::min(res, i - pos[b]);
                b++;
            }
            while (b < e && sp <= st_s[e - 1])
                e--;
            st_s[e] = sp;
            pos[e++] = i;
        }
        if (res == n + 1)
            return -1;
        return res;
    }
};
```