# Successful Pairs of Spells and Potions

[题目](https://leetcode.com/problems/successful-pairs-of-spells-and-potions/description/)

正常情况下看了提示应该就会写了：

```
Notice that if a spell and potion pair is successful, then the spell and all stronger potions will be successful too.

Thus, for each spell, we need to find the potion with the least strength that will form a successful pair.

We can efficiently do this by sorting the potions based on strength and using binary search.
```

我没用binary search，尝试直接遍历。倒也没有TLE，直接错误答案。大概是因为我没有把int转long再相乘吧。

```c#
//https://leetcode.com/problems/successful-pairs-of-spells-and-potions/solutions/3367914/easy-solutions-in-java-python-and-c-look-at-once-with-exaplanation/
class Solution {
    public int[] SuccessfulPairs(int[] spells, int[] potions, long success) {
        int n = spells.Length;
        int m = potions.Length;
        int[] pairs = new int[n];
        Array.Sort(potions);
        for (int i = 0; i < n; i++) {
            int spell = spells[i];
            int left = 0;
            int right = m - 1;
            while (left <= right) {
                int mid = left + (right - left) / 2;
                long product = (long) spell * potions[mid];
                if (product >= success) {
                    right = mid - 1;
                } else {
                    left = mid + 1;
                }
            }
            pairs[i] = m - left;
        }
        return pairs;
    }
}
```

```
Runtime
359 ms
Beats
81.82%
Memory
63 MB
Beats
22.73%
```

但是换个思路想，是否可以不用pairs数组，直接放在spells里呢？甚至说，根本不用Array.Sort或者binary search？

```c#
//https://leetcode.com/problems/successful-pairs-of-spells-and-potions/solutions/3368209/prefix-postfix-sum-c-99-faster-in-time/
class Solution {
    public int[] SuccessfulPairs(int[] spells, int[] potions, long success) {
        int[] postfix = new int[100001];
        foreach(int potion in potions) postfix[potion]++;
        for(int i=99999; i>=0; --i) postfix[i] += postfix[i+1];

        //No need extra space at all for storing final result
        for(int i=0; i<spells.Length; ++i){
            long val = success / (long) spells[i];
            if(success % (long) spells[i] != 0) val++;

            spells[i] = val <= 1e5 ? postfix[val] : 0;//这个1e5表示10的5次方，题目的constraints里面有写任意potions[i]一定小于这个数
        }
        return spells;
    }
}
```

```
Runtime
345 ms
Beats
95.45%
Memory
62.5 MB
Beats
31.82%
```