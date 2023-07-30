# Soup Servings

[题目](https://leetcode.com/problems/soup-servings/description/)

这是数学题。特别是当发现discussion区一个神奇的if条件后，数学成分更浓了。
```c#
//采样区，类似 https://leetcode.com/problems/soup-servings/editorial/ 的第二种递归做法
public class Solution {
    public double SoupServings(int n) {
        if(n > 4800){ //参考discussion区 Shubham_Raj22的评论
        //详细数学证明： https://leetcode.com/problems/soup-servings/solutions/195582/a-mathematical-analysis-of-the-soup-servings-problem/
            return 1;
        }
        return SoupServe(n,n, new());
    }
    public double SoupServe(int a, int b, Dictionary<string,double> memo){
        if(a <= 0 && b <= 0){ //两种汤一起没，根据描述，取概率的一半
            return .5;
        }
        if(b <= 0){ //b先没且a没有没，那么a先没的概率是0%
            return 0;
        }
        if(a <= 0){ //反之100%
            return 1.0;
        }
        string current_str = a.ToString() + ' ' + b.ToString(); //利用a的剩余+b的剩余作为memo的键
        if(memo.ContainsKey(current_str)){
            return memo[current_str];
        }
        double prob = 0;
        prob += SoupServe(a - 100 , b, memo); //4种情况都试一遍
        prob += SoupServe(a-75, b-25, memo);
        prob += SoupServe(a-50, b-50, memo);
        prob += SoupServe(a-25, b-75, memo);
        memo[current_str] = prob/4; //别忘了每种操作都是25%的概率
        return prob / 4;
    }
}
```
```
Runtime
17 ms
Beats
100%
Memory
29.5 MB
Beats
14.29%
```