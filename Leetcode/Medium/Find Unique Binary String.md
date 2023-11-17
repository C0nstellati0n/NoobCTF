# [Find Unique Binary String](https://leetcode.com/problems/find-unique-binary-string)

啊？我一下就想出了最佳解法？不对吧？
```c++
class Solution {
public:
    string findDifferentBinaryString(vector<string>& nums) {
        string ans="";
        for(int i=0;i<nums.size();i++){
            if(nums[i][i]=='0') ans+="1";
            else ans+="0";
        }
        return ans;
    }
};
```
参考[editorial](https://leetcode.com/problems/find-unique-binary-string/editorial)，众多解法中这种是最好的。跟[Cantor's diagonal argument](https://en.wikipedia.org/wiki/Cantor%27s_diagonal_argument)有关。Cantor's diagonal argument说明了自然数是无限的，因此提供了一种从有限集合中创造集合中未出现过的数的方法。但是我做的时候没想那么多，我就想：“要找一个没出现过的数，那只要至少有一位与各个数不同就好了”。自然而然就想到对角线了