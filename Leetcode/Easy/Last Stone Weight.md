# Last Stone Weight

[题目](https://leetcode.com/problems/last-stone-weight/description/)

这题涉及到[堆](https://www.jianshu.com/p/6b526aa481b1)（heap，也叫优先队列（priority queue））数据结构。

```c#
//https://leetcode.com/problems/last-stone-weight/solutions/3448695/python-java-c-simple-solution-easy-to-understand/
class Solution {
    public int LastStoneWeight(int[] stones) {
        //https://stackoverflow.com/questions/71306396/use-lambda-comparator-with-priorityqueue
        PriorityQueue<int,int> maxHeap = new(Comparer<int>.Create((x, y) => y-x));//递降排序,似乎必须两个参数
        foreach(int stone in stones) {
            maxHeap.Enqueue(stone,stone);
        }
        while (maxHeap.Count != 1) {
            int stone1 = maxHeap.Dequeue();
            int stone2 = maxHeap.Dequeue();
            maxHeap.Enqueue(Math.Abs(stone1 - stone2),Math.Abs(stone1 - stone2));
        }
        return maxHeap.Dequeue();
    }
}
```

```
Runtime
77 ms
Beats
93.27%
Memory
38.2 MB
Beats
29.53%
```

c#中的[priority queue](https://learn.microsoft.com/zh-cn/dotnet/api/system.collections.generic.priorityqueue-2?view=net-7.0)据说近几年才加入，我对这个类可以说是完全不熟。翻了文档，发现初始化时需要一个Comparer，用于计算队列中每个元素的优先度。而且添加元素时还要把优先级作为第二个参数。但是这题的优先级就是元素本身的值啊，似乎有点复杂了，直接list也行。

```c#
public class Solution {
    public int LastStoneWeight(int[] stones) {
        return Game(stones.ToList()); 
    }
    public int Game(List<int> stones) {
        if(stones.Count == 1) return stones[0];

        stones.Sort();

        var battleResult = stones[stones.Count-1] - stones[stones.Count-2];
 
        if(stones.Count == 2 && battleResult == 0) return 0;

        stones.RemoveAt(stones.Count - 2);
        stones.RemoveAt(stones.Count - 1);
        
        if(battleResult != 0) { 
           stones.Add(battleResult);
        } 
        return Game(stones);
    }   
}
```

```
Runtime
78 ms
Beats
91.81%
Memory
37.8 MB
Beats
74.27%
```

直接array也行。

```c#
public class Solution {
    public int LastStoneWeight(int[] stones) {
        
        while(stones.Length > 1)
        {
            Array.Sort(stones);
            if(stones[stones.Length - 1] == stones[stones.Length - 2])
            {
                Array.Resize(ref stones, stones.Length - 2);
            }
            else if(stones[stones.Length - 1] != stones[stones.Length - 2])
            {
                stones[stones.Length - 2] = stones[stones.Length - 1] - stones[stones.Length - 2];
                Array.Resize(ref stones, stones.Length - 1);
            }
           
        }
        if(stones.Length == 0)
        {
            return 0;
        }
        return stones[0];
    }
}
```

```
Runtime
82 ms
Beats
80.41%
Memory
38 MB
Beats
46.78%
```