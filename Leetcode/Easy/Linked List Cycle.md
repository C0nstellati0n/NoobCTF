# Linked List Cycle

[题目](https://leetcode.com/problems/linked-list-cycle/description/)

我知道Floyd Cycle Detection Algorithm的，但是忘了用了。
```c#
public class Solution {
    public bool HasCycle(ListNode head) {
        if(head==null){
            return false;
        }
        List<ListNode> record=new();
        while(head.next!=null){
            if(record.Contains(head)){
                return true;
            }
            record.Add(head);
            head=head.next;
        }
        return false;
    }
}
```
```
Runtime
648 ms
Beats
5.7%
Memory
43.7 MB
Beats
31.56%
```
我也没想到这居然不tle啊？接下来是正确做法。
```c#
//采样区
//solution有人叫这种算法为2 pointers或者slow&fast
public class Solution {
    public bool HasCycle(ListNode head) {
        if (head == null)
        {
            return false;
        }
        var p1 = head;
        var p2 = head.next;
        while (true)
        {
            if (p2 == null || p2.next == null)
            {
                return false;
            }
            //原理很简单，拿两个pointer，一个每次走一步，另一个每次走两步。假如链表有环的话，它们肯定会相遇
            if (p1 == p2)
            {
                return true;
            }

            p1 = p1.next;
            p2 = p2.next.next;
        }
    }
}
```
```
Runtime
92 ms
Beats
72.58%
Memory
43.2 MB
Beats
55.39%
```
还有一个我不太懂的做法。说是把链表反转，要是有环的话反转后的head和原来是一样的。为啥？
```c#
//https://leetcode.com/problems/linked-list-cycle/solutions/44498/just-reverse-the-list/
public class Solution {
    ListNode reverseList(ListNode head) 
    {
        ListNode prev = null;
        ListNode follow = null;
        while (head!=null)
        {
            follow = head.next;
            head.next = prev;
            prev = head;
            head = follow;
        }
        return prev;
    }
    public bool HasCycle(ListNode head)
    {
        ListNode rev = reverseList(head);
        if (head!=null && head.next!=null && rev == head)
        {
            return true;
        }
        return false;
    }
}
```
```
Runtime
83 ms
Beats
94.39%
Memory
42.9 MB
Beats
80.1%
```