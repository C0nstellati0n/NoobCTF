# [Minimum One Bit Operations to Make Integers Zero](https://leetcode.com/problems/minimum-one-bit-operations-to-make-integers-zero)

抄别人的思路抄出个wrong answer……
```c++
class Solution {
public:
    int minimumOneBitOperations(int n) {
        int ans=0;
        int index=1;
        int right=0;
        while(n!=0){
            if(n&1){
                ans=pow(2,index)-1-ans;
            }
            index++;
            n>>=1;
        }
        return ans;
    }
};
```
和editorial有点不一样，因为i最开始看了discussion区khoshmard的评论后就直接冲了，结果发现搞错了ans的规律。于是去editorial抄了个规律。规律是把数字拆成若干个2的n次方：1010=1000+0010，将2的n次方bit转为0需要 $2^{n+1}-1$ 次操作。这些2的n次方所组成的数字所需操作为 $2^{n+1}-1-A(n')$ ，n'是从右往左数时上一个1 bit处的结果

还有一个做法是用[Gray code](https://en.wikipedia.org/wiki/Gray_code)。这题的要求恰好和构造n的gray code重合，所以直接用gray code的算法即可