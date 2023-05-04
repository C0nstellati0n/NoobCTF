# Dota2 Senate

[题目](https://leetcode.com/problems/dota2-senate/description/)

又是一道一看就会，但是看答案之前死活不会的题。

```c#
//https://leetcode.com/problems/dota2-senate/solutions/3483354/image-explanation-fastest-easiest-concise-c-java-python/
class Solution {
    public string PredictPartyVictory(string senate) {
        Queue<int> qr = new();
        Queue<int> qd = new();
        int n = senate.Length;

        for (int i = 0; i < n; i++) {
            if (senate[i] == 'R') {
                qr.Enqueue(i);
            } else {
                qd.Enqueue(i);
            }
        }

        while (qr.Count!=0 && qd.Count!=0) {
            int r_id = qr.Dequeue();
            int d_id = qd.Dequeue();
            if (r_id < d_id) {
                qr.Enqueue(r_id + n);
            } else {
                qd.Enqueue(d_id + n);
            }
        }

        return (qr.Count > qd.Count) ? "Radiant" : "Dire";
    }
}
```

```
Runtime
78 ms
Beats
98%
Memory
39.3 MB
Beats
54%
```

题目描述里有一句“Suppose every senator is smart enough and will play the best strategy for his own party. ”。于是我就懵了，啥是best strategy？每位senator都有两种操作，ban掉地方阵营下一位senator，或是宣布胜利。被ban的senator则无法宣布胜利。后面意识到，best strategy就是一股脑地ban对面senator，直到场上只剩下自己的人。

如果这样的话就不难理解了。程序一开始先来个for循环，将各方的索引推入队列。因为小的id会ban掉大的id，所以while循环里只将更小的id重新入队列。这样一轮一轮下去，直到最后有一方全部被ban掉后，剩下的一方就可以宣布胜利了。