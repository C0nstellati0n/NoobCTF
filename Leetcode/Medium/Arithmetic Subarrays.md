# [Arithmetic Subarrays](https://leetcode.com/problems/arithmetic-subarrays)

以为hint是给出思路，真正做法不可能直接爆破。结果hint一层反套路都不打
```c++
class Solution {
public:
    vector<bool> checkArithmeticSubarrays(vector<int>& nums, vector<int>& l, vector<int>& r) {
        vector<bool> ans;
        for(int i=0;i<l.size();i++){
            ans.push_back(check(nums,l[i],r[i]));
        }
        return ans;
    }
    bool check(vector<int> nums,int l,int r){
        if(nums.size()<=2) return true;
        sort(nums.begin()+l,nums.begin()+r+1);
        int first=nums[l+1]-nums[l];
        for(int i=l+2;i<r+1;i++){
            if(nums[i]-nums[i-1]!=first) return false;
        }
        return true;
    }
};
```
editorial还有个不用sort的做法，理论时间复杂度比这个更低，但是实际submit的表现直逼200ms，我这个笨蛋sort都不到60ms
```c++
//这个做法也是不用sort，但是干到28ms就离谱
//https://leetcode.com/problems/arithmetic-subarrays/solutions/910421/c-two-approaches-140-vs-28ms
class Solution {
public:
    vector<bool> checkArithmeticSubarrays(vector<int>& nums, vector<int>& l, vector<int>& r) {
        vector<bool> res;
        for (auto i = 0, j = 0; i < l.size(); ++i) {
            auto [p_min, p_max] = minmax_element(begin(nums) + l[i], begin(nums) + r[i] + 1); //原来c++有自带的找最大最小元素的函数
            int len = r[i] - l[i] + 1, d = (*p_max - *p_min) / (len - 1);
            if (*p_max == *p_min)
                res.push_back(true);
            else if ((*p_max - *p_min) % (len - 1)) //假如这个是一个ArithmeticSubarray，就有关系An=A0+(n-1)*d。那么An-A0模n-1一定为0。不过ArithmeticSubarray一定满足这个条件，但满足这个条件不一定是ArithmeticSubarray
                res.push_back(false);
            else {
                vector<bool> n(len);
                for (j = l[i]; j <= r[i]; ++j) {
                    if ((nums[j] - *p_min) % d || n[(nums[j] - *p_min) / d]) //所以下面还要继续检查其他的元素是否满足上面提到的特征
                        break;
                    n[(nums[j] - *p_min) / d] = true; //p_min和d都是固定的，只要nums[j]不重复，应该就不会在上面的if语句被刷下来。一旦重复了就不可能是ArithmeticSubarray
                }
                res.push_back(j > r[i]);
            }
        }
        return res;
    }
};
```