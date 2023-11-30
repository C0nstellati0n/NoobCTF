# [Number of 1 Bits](https://leetcode.com/problems/number-of-1-bits)

过于无脑
```c++
class Solution {
public:
    int hammingWeight(uint32_t n) {
        return __builtin_popcount(n);
    }
};
```
或者用 https://leetcode.com/problems/number-of-1-bits/solutions/55255/c-solution-n-n-1 里的trick
```c++
class Solution {
public:
    int hammingWeight(uint32_t n) {
        int c=0;
        while(n)
        {
            n = n&(n-1);
            c++;
        }
        return c;
    }
};
```