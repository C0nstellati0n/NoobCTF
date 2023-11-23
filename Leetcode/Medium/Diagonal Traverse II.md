# [Diagonal Traverse II](https://leetcode.com/problems/diagonal-traverse-ii)

帮帮我，priority_queue!
```c++
//如何自定义比较器： https://stackoverflow.com/questions/16111337/declaring-a-priority-queue-in-c-with-a-custom-comparator
class Compare{
public:
    bool operator()(const tuple<int,int,int>& a,const tuple<int,int,int>& b){
        if(get<0>(a)==get<0>(b)){
            return get<1>(a)<get<1>(b);
        }
        return get<0>(a)>get<0>(b);
    }
};
class Solution {
public:
    vector<int> findDiagonalOrder(vector<vector<int>>& nums) {
        priority_queue<tuple<int,int,int>,vector<tuple<int,int,int>>, Compare> pq;
        for(int i=0;i<nums.size();i++){
            for(int j=0;j<nums[i].size();j++){
                pq.push(make_tuple(i+j, i, nums[i][j]));
            }
        }
        vector<int> ans;
        while (!pq.empty()) {
            ans.push_back(get<2>(pq.top()));
            pq.pop();
        }
        return ans;
    }
};
```
看了提示就知道该按照什么顺序排序了。这题还可以看做bfs，参考[editorial](https://leetcode.com/problems/diagonal-traverse-ii/editorial)，不过相同的做法采样区更快
```c++
//愿将这段称为提速魔法，看见过好多次了
#pragma GCC optimize("Ofast","inline","-ffast-math")
#pragma GCC target("avx,mmx,sse2,sse3,sse4")
static const int _ = []() { std::ios::sync_with_stdio(false); std::cin.tie(nullptr); std::cout.tie(nullptr); return 0; }();
class Solution
{
public:
    vector<int> findDiagonalOrder(vector<vector<int>> &nums)
    {
        int n = nums.size();
        queue<pair<int, int>> q;
        q.emplace(make_pair(0, 0));
        vector<int> res;
        while(!q.empty())
        {
            pair<int, int> it = q.front(); //first是row，second是column
            q.pop();
            res.emplace_back(nums[it.first][it.second]);
            if(it.second == 0 && it.first < n - 1) //按照斜边扩张时，col为0的既往下也往右扩张
            {
                q.emplace(make_pair(it.first + 1, it.second));
            }
            if(it.second + 1 < nums[it.first].size()) //剩余只往右扩张。同时保证不越索引
            {
                q.emplace(make_pair(it.first, it.second + 1));
            }
        }
        return res;
    }
};
```