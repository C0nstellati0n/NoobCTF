# Implement Stack using Queues

[题目](https://leetcode.com/problems/implement-stack-using-queues/description/)

c#：我们给大家提供了stack，queue，priority queue等数据结构！不敢想象大家会用它们写出什么厉害的东西！

我：今天咱们来用priority queue实现stack
```c#
public class MyStack {
    PriorityQueue<int,int> q;
    int index;
    public MyStack() {
        q=new();
        index=0;
    }
    
    public void Push(int x) {
        q.Enqueue(x,-index);
        index++;
    }
    
    public int Pop() {
        return q.Dequeue();
    }
    
    public int Top() {
        return q.Peek();
    }
    
    public bool Empty() {
        return q.Count==0;
    }
}
```
```
Runtime
99 ms
Beats
79.3%
Memory
40.4 MB
Beats
87.10%
```
说实话PriorityQueue不是特别好，它的时间复杂度好像是O(n log(n))？一个普通队列完全可以用。
```c#
//https://leetcode.com/problems/implement-stack-using-queues/solutions/62527/a-simple-c-solution/
public class MyStack {
    Queue<int> que=new();
	public void Push(int x) {
		que.Enqueue(x);
		for(int i=0;i<que.Count-1;++i){
			que.Enqueue(que.Peek());
			que.Dequeue();
		}
	}
	public int Pop() {
		return que.Dequeue();
	}
	public int Top() {
		return que.Peek();
	}
	public bool Empty() {
		return que.Count==0;
	}
}
```
```
Runtime
96 ms
Beats
88.6%
Memory
40.8 MB
Beats
31.29%
```