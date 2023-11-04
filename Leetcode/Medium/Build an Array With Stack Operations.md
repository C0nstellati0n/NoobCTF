# [Build an Array With Stack Operations](https://leetcode.com/problems/build-an-array-with-stack-operations)

这个真的不算medium
```c++
class Solution {
public:
    vector<string> buildArray(vector<int>& target, int n) {
        vector<string> ans;
        int index=0;
        for(int i=1;i<=n;i++){
            if(index>=target.size()) break;
            if(target[index]==i){
                ans.push_back("Push");
                index++;
            }
            else{
                ans.push_back("Push");
                ans.push_back("Pop");
            }
        }
        return ans;
    }
};
```
我尝试遍历n，还可以遍历target，参考[editorial](https://leetcode.com/problems/build-an-array-with-stack-operations/editorial)