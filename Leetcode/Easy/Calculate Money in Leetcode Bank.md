# [Calculate Money in Leetcode Bank](https://leetcode.com/problems/calculate-money-in-leetcode-bank)

这波属于是我格局小了
```c++
class Solution {
public:
    int totalMoney(int n) {
        int start=1;
        int res=0;
        while(n-7>=0){
            res+=((start+(start+6))*7)/2;
            start++;
            n-=7;
        }
        res+=((start+(start+n-1))*n)/2;
        return res;
    }
};
```
discussion区都在说什么[Arithmetic progression](https://en.wikipedia.org/wiki/Arithmetic_progression)，我一看，原来是数列啊。每周（除了最后那些多出来了）都是一个长度为7的数列，那么直接套用公式算出每周的金币数量然后加起来即可

但是我去看了 https://leetcode.com/problems/calculate-money-in-leetcode-bank/solutions/1009171/faster-than-100-00-commented-java-cpp-c 的评论区，恍然大悟，数列并不只局限于每周每天的金币数量，每周整体的金币数量也是。不好解释，直接看代码
```c++
class Solution {
public:
    int totalMoney(int n) {
        //completeWeek indicates how many complete week Hercy added money
        //to the bank.
        int completeWeek = n / 7;  
        //leftDays indicates number of left days after completeWeek turn.
        int leftDays = n % 7;
        //starting money in the last week
        int startMoney = completeWeek + 1;
        //sum of AP series : Sn = (n * [2 * a + (n - 1) * d]) / 2
        int completeWeekMoneysum = (completeWeek * (2 * 28 + (completeWeek - 1) * 7)) / 2; //这里套用了两个公式，已知首项计算第n项的公式，和整体求和公式:an=a1+(n-1)d ; sum=(n(a1+an))/2 。就有 sum=(n(a1+(a1+(n-1)d)))/2=(n(2a1)+(n-1)d)/2
        int leftDaysMoneySum = (leftDays * (2 * startMoney + (leftDays - 1))) / 2; //这个同理，不过这里不满一周，每项之间的差值是1
        return (completeWeekMoneysum + leftDaysMoneySum);
    }
};
```