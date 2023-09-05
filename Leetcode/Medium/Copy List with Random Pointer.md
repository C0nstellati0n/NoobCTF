# Copy List with Random Pointer

[题目](https://leetcode.com/problems/copy-list-with-random-pointer)

这题的难点在于random pointer。假如就是个linked list的话，随便copy。但是出来个random pointer就有点难搞了，假如我们在copy 1号node，它的random pointer却指向了还没copy的3号node，该怎么办？收集了不同做法，邀诸位共赏。
```c#
//采样区，不过我找了个解析： https://leetcode.com/problems/copy-list-with-random-pointer/solutions/4003262/97-92-hash-table-linked-list/
//使用字典
public class Solution {
     public Node CopyRandomList(Node head) {
         if ( head == null){
             return null;
         }
         Dictionary<Node,Node> dict = new();
         var current = head;
         while ( current != null){ //关键点在于提前遍历一遍linked list，记录所有的node对应的copy node
             dict[current] = new Node(current.val);
             current = current.next;
         }
         Node newHead = new Node(0);
         Node temp = newHead;
         current = head;
         while ( current != null){
             temp.next= dict[current];
             if ( current.random != null){ //于是在后面设置random pointer时就不用担心node还没copy了，前面都已经copy完了
                 temp.next.random = dict[current.random];
             }
             temp = temp.next;
             current = current.next;
         }
         temp.next = null;
         return newHead.next;
     }
}
```
```
Runtime
78 ms
Beats
91.83%
Memory
39.8 MB
Beats
34.81%
```
然后还有两种均来自 https://leetcode.com/problems/copy-list-with-random-pointer/solutions/43497/2-clean-c-algorithms-without-using-extra-array-hash-table-algorithms-are-explained-step-by-step ，这个solution评论区有大佬发了图片，一目了然。
```c#
//但是这个实现我是在这里找的： https://leetcode.com/problems/copy-list-with-random-pointer/solutions/43491/a-solution-with-constant-space-complexity-o-1-and-linear-time-complexity-o-n/ ，java改的比较方便。一样思路
//交织node从而只用O(1)空间
public class Solution {
    public Node CopyRandomList(Node head) {
        Node iter = head, next;
        // First round: make copy of each node,
        // and link them together side-by-side in a single list.
        Node copy;
        while (iter != null) { //这个while循环copy node并将原node和其copy交织在一起。如1的copy是1',这里构造形如1->1'->2->2'的linked list
            next = iter.next;
            copy = new(iter.val);
            iter.next = copy;
            copy.next = next;
            iter = next;
        }
        // Second round: assign random pointers for the copy nodes.
        iter = head;
        while (iter != null) {
            if (iter.random != null) { //与第一种做法类似，上面copy过node了，不用担心random pointer指向的node没copy过
                iter.next.random = iter.random.next; //iter表示原node,iter.next表示其copy。所以iter.random.next表示原node的random的copy。若只写iter.next.random = iter.random，那iter的copy node的random指向的就是原本node的random了，不是copy的
            }
            iter = iter.next.next;
        }
        // Third round: restore the original list, and extract the copy list.
        iter = head;
        Node pseudoHead = new Node(0);
        Node copyIter = pseudoHead;
        while (iter != null) { //把交织在一起的node分离开
            next = iter.next.next;
            // extract the copy
            copy = iter.next;
            copyIter.next = copy;
            copyIter = copy;
            // restore the original list
            iter.next = next;
            iter = next;
        }
        return pseudoHead.next;
    }
}
```
```
Runtime
71 ms
Beats
98.58%
Memory
39.8 MB
Beats
55.42%
```
```c#
//构造与原node一一对应的copy node（两个linked list）
//利用copy的next记录原node的random，原node的random保存其对应的copy
public class Solution {
    public Node CopyRandomList(Node head) {
        if (head == null) return null;
        Node newHead, l1, l2;
        for (l1 = head; l1 != null; l1 = l1.next) {
            l2 = new Node(l1.val); //copy每个node
            l2.next = l1.random; //copy node的next帮忙记录node的random
            l1.random = l2; //原来的random改为记录其对应的copy node
        }     
        newHead = head.random; //newHead为head的copy node
        for (l1 = head; l1 != null; l1 = l1.next) {
            l2 = l1.random; //取出每个node对应的copy node
            l2.random = l2.next!=null ? l2.next.random : null; //判断l2.next是否为null。若不为null，l2.next记录的是其对应的原node的random。用l2.next取得。这个取到的node是原node，其对应的copy node为random。于是l2.next.random
        }
        for (l1 = head; l1 != null; l1 = l1.next) {
            l2 = l1.random; //恢复原链表的random
            l1.random = l2.next;
            l2.next = l1.next!=null ? l1.next.random : null; //以及更新复制链表的next
        }
        return newHead;
    }
}
```
```
Runtime
74 ms
Beats
97.87%
Memory
39.5 MB
Beats
83.48%
```
不难看出关键在于先把node全copy完了再慢慢处理node。