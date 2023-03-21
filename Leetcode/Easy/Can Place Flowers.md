# Can Place Flowers

[题目](https://leetcode.com/problems/can-place-flowers/description/)

发现我的脑回路蠢得清奇。这题会给一个花田和要插花的数量n，要求插的花不能相邻。如果花田能插下n朵花，就返回True；否则返回False。花田用1表示有花，0表示空闲。我的想法是什么呢？我竟然想着按照1的出现位置把花田分成几份，一份一份地数。也不是说不行，但花田的开始和末尾是特殊情况，用我的思路写就会非常难写。实际上哪有这么复杂，这是道简单题，直接遍历着看不就完了吗？

```c#
//https://leetcode.com/problems/can-place-flowers/solutions/3317843/java-c-simple-solution-easy-to-understand/
class Solution {
    public bool CanPlaceFlowers(int[] flowerbed, int n) {
        if (n == 0) {
            return true;
        }
        for (int i = 0; i < flowerbed.Length; i++) {
            if (flowerbed[i] == 0 && (i == 0 || flowerbed[i-1] == 0) && (i == flowerbed.Length-1 || flowerbed[i+1] == 0)) {
                flowerbed[i] = 1;
                n--;
                if (n == 0) {
                    return true;
                }
            }
        }
        return false;
    }
}
```

```
Runtime
98 ms
Beats
98.89%
Memory
45.6 MB
Beats
53.59%
```