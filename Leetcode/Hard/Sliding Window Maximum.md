# Sliding Window Maximum

[题目](https://leetcode.com/problems/sliding-window-maximum/description/)

hint1: 建议用某种数据结构，比如说双端队列。

我：emmm什么是双端队列？不过有点理解，用队列记录window宽度那么多的元素，然后算……

hint2: The queue size need not be the same as the window’s size.

我：啊？
```java
//今天只有java，因为c#里没有deque
//与 https://leetcode.com/problems/sliding-window-maximum/editorial/ 思路与做法一致，不过这种速度更快
//https://jadi.net/wp-content/uploads/2017/07/competetive-programmers-handbook.pdf#page=91 也有讲解
class Solution {
    public int[] maxSlidingWindow(int[] a, int k) {		
		if (a == null || k <= 0) {
			return new int[0];
		}
		int n = a.length;
		int[] r = new int[n-k+1];
		int ri = 0;
		// store index
        //基本思路：记录一个q，q的第一个元素是window的最后一个元素，q的最后一个元素是window中最大的元素。q中越靠近队列头的元素越大。不过这里记录index，方便将window范围之外的元素拿出去
		Deque<Integer> q = new ArrayDeque<>(); //java双端队列
		for (int i = 0; i < a.length; i++) {
			// remove numbers out of range k
			while (!q.isEmpty() && q.peek() < i - k + 1) {
				q.poll(); //poll：移除队列头的元素
			}
			// remove smaller numbers in k range as they are useless
			while (!q.isEmpty() && a[q.peekLast()] < a[i]) {
				q.pollLast(); ///pollLast：移除q中的最后一个元素（队列尾）
			}
			// q contains index... r contains content
			q.offer(i); //往队列尾添加元素
			if (i >= k - 1) {
				r[ri++] = a[q.peek()]; //添加最大的元素
			}
		}
		return r;
	}
}
```
```
Runtime
30 ms
Beats
86.65%
Memory
59.5 MB
Beats
70.39%
```
我看那个pdf时一直困于如何将超出window范围的元素移出队列。看了大佬的做法后才明白过来。不要直接添加元素，添加索引即可，拿这个索引再去nums里取元素。还有另一种我直呼天才的做法： https://leetcode.com/problems/sliding-window-maximum/solutions/65881/o-n-solution-in-java-with-two-simple-pass-in-the-array/ ，不过这里面没啥新的数据结构，而且有点数学（要证明），就不记录了