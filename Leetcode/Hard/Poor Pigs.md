# [Poor Pigs](https://leetcode.com/problems/poor-pigs)

数学题。另外我抄答案的时候run按成submit了，寄
```c#
//采样区
//https://leetcode.com/problems/poor-pigs/solutions/94266/another-explanation-and-solution 的优化版本，但是思路是一样的
public class Solution {
    /*
    p1=2^p1
    p2=2^p2 * 2^p1
    */
    public int PoorPigs(int buckets, int minutesToDie, int minutesToTest) {
        if(buckets<2){
            return 0;
        }
        int n=1;
        int c=1;
        int x=1+(minutesToTest/minutesToDie);
        while(x*n<buckets){
            n=x*n;
            c++;
        }
        return c;
    }
}
```