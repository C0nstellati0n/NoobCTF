# [Reduction Operations to Make the Array Elements Equal](https://leetcode.com/problems/reduction-operations-to-make-the-array-elements-equal)

这题大家想法都挺统一的，唯一的不同不过是最开始排序时到底是直接排序数组还是用counting sort。我用的是counting sort
```c++
class Solution {
public:
    int reductionOperations(vector<int>& nums) {
        int freq[50001]={0};
        for(int num:nums){
            freq[num]++;
        }
        int ans=0;
        int temp=0;
        for(int i=50000;i>=1;i--){
            if(freq[i]!=0){
                temp+=freq[i];
                ans+=temp;
            }
        }
        ans-=temp;
        return ans;
    }
};
```
[editorial](https://leetcode.com/problems/reduction-operations-to-make-the-array-elements-equal/editorial)用的是直接sort。运行用时counting sort更好，直接sort内存更好