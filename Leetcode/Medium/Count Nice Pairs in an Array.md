# [Count Nice Pairs in an Array](https://leetcode.com/problems/count-nice-pairs-in-an-array)

遍历字典的for循环后面忘记加大括号了，自己找了好久都没找到这里。还是去问AI才知道
```c++
class Solution {
public:
    int countNicePairs(vector<int>& nums) {
        unordered_map<int,long> map;
        int mod=(int)1e9+7;
        for(int num:nums){
            map[num-rev(num)]++;
        }
        long ans=0;
        for (auto const& [key, value] : map){
            ans=(ans+value*(value-1)/2)%mod; //permutation计算公式
        }
        return ans;
    }
private:
    int rev(int num) 
    { 
        int rev_num = 0; 
        while (num > 0) { 
            rev_num = rev_num * 10 + num % 10; 
            num = num / 10; 
        } 
        return rev_num; 
    }
};
```
之前其实也做过类似的permutation题，所以也可以一边计算frequency一边加，不用额外遍历字典。这里拿采样区大佬的解法，因为真的很快
```c++
class Solution {
public:
    int countNicePairs(vector<int>& nums) {
        ios_base::sync_with_stdio(false);
		cin.tie(0);
		cout.tie(0); //就是这三句让这个解法比较快。参考 https://stackoverflow.com/questions/31162367/significance-of-ios-basesync-with-stdiofalse-cin-tienull
        unordered_map<int,int> mp;
        long long ans = 0;
        for(int num:nums) {
            int dup = num;
            int rev = 0;
            while(dup>0) {
                rev = rev*10 + dup%10;
                dup = dup/10;
            }
            ans+= mp[(num-rev)]; //一边计算一边加
            ans = ans%1000000007;
            mp[(num-rev)]++;
        }
        return ans;
    }
};
```
所以这题的关键点在于hint。只要看了hint就知道咋做了