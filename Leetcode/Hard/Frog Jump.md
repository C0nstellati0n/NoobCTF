# Frog Jump

[Frog Jump](https://leetcode.com/problems/frog-jump/description/)

这题我自己写了一个小时都要写疯了。事实证明方向正确比努力更重要，应该用二维的dp我用成一维了。[editorial](https://leetcode.com/problems/frog-jump/editorial/)还是常规地记录了递归dp和遍历dp的做法。

不过采样区的类似bfs的做法引起了我的注意。
```c#
public class Solution {
    public bool CanCross(int[] stones) {
        int n = stones.Length;
        var dict = new Dictionary<int, int>();
        for(int i = 0; i < n; ++i) {
            dict.Add(stones[i], i);
        }

        var queue = new PriorityQueue<(int i, int k), int>();
        queue.Enqueue((0, 0), 0); //queue的元素是一个记录(index,step)的tuple，优先度为index。从下面的queue.Enqueue((index, k + i), -index); 可得出是倒序排序

        var result = false;
        var steps = 2 * n * 3; //因为这个bfs没有visited，所以需要个循环次数的上限。不懂这是咋求出来的

        while(queue.Count > 0 && steps-- > 0) {
            var s = queue.Dequeue();
            if (s.i == n - 1) { //能够到达最后一块石头，返回true
                result = true;
                break;
            }
            var k = s.k;

            var pos = stones[s.i]; //当前所在的石头的数字
            for (int i = 1; i >= -1; --i) { //尝试全部的跳跃可能k-1,k,k+1
                if (dict.ContainsKey(pos + k + i)) { //若该石头存在
                    var index = dict[pos + k + i];
                    queue.Enqueue((index, k + i), -index); //则新的石头如队列
                }
            }
        }

        return result;
    }
}
```
```
Runtime
93 ms
Beats
100%
Memory
46.8 MB
Beats
100%
```
比较常规的dp题。但是dp的维数很重要啊！