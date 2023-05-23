# Kth Largest Element in a Stream

[题目](https://leetcode.com/problems/kth-largest-element-in-a-stream/description/)

我的解法和大佬们的相差无几。

```c#
public class KthLargest {
    PriorityQueue<int,int> heap = new(Comparer<int>.Create((x, y) => x-y));
    int k;
    public KthLargest(int k, int[] nums) {
        this.k=k;
        foreach(int num in nums){
            heap.Enqueue(num,num);
        }
        while(heap.Count>k){
            heap.Dequeue();
        }
    }
    
    public int Add(int val) {
        if(heap.Count<k){
            heap.Enqueue(val,val);
        }
        else if(val>=heap.Peek()){
            heap.Enqueue(val,val);
            heap.Dequeue();
        }
        return heap.Peek();
    }
}
```
```
Runtime
142 ms
Beats
95.74%
Memory
59.1 MB
Beats
40.31%
```
还看见一个用TreeNode（BST）的解法：https://leetcode.com/problems/kth-largest-element-in-a-stream/solutions/147729/o-h-java-solution-using-bst/