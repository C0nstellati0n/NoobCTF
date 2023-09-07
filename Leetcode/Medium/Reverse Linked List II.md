# Reverse Linked List II

[题目](https://leetcode.com/problems/reverse-linked-list-ii/description)

本来想记点笔记的。但是linked list说再多的话也不如看图。于是我找了个有图解的solution
```c#
//https://leetcode.com/problems/reverse-linked-list-ii/solutions/2311084/java-c-tried-to-explain-every-step
//建议旁边放代码然后跟图一个一个看。有点绕
class Solution {
    public ListNode ReverseBetween(ListNode head, int left, int right) {
        ListNode dummy = new ListNode(0); // created dummy node
        dummy.next = head;
        ListNode prev = dummy; // intialising prev pointer on dummy node
        for(int i = 0; i < left - 1; i++)
            prev = prev.next; // adjusting the prev pointer on it's actual index
        ListNode curr = prev.next; // curr pointer will be just after prev
        // reversing
        for(int i = 0; i < right - left; i++){
            ListNode forw = curr.next; // forw pointer will be after curr
            curr.next = forw.next;
            forw.next = prev.next;
            prev.next = forw;
        }
        return dummy.next;
    }
}
```
```
Runtime
70 ms
Beats
96.60%
Memory
38.6 MB
Beats
32.72%
```
还有另一种大同小异的做法，我在 https://leetcode.com/problems/reverse-linked-list-ii/solutions/30666/simple-java-solution-with-clear-explanation 的评论区找到的。
```c#
public class Solution {
    public ListNode ReverseBetween(ListNode head, int m, int n) {
        ListNode fakeHead = new ListNode(-1);
        fakeHead.next = head;
        ListNode prev = fakeHead;
        ListNode curr = fakeHead.next;
        int i = 1;
        while (i < m) {
            prev = curr;
            curr = curr.next;
            i++;
        }
        ListNode node = prev;
        while (i <= n) {
            ListNode tmp = curr.next;
            curr.next = prev;
            prev = curr;
            curr = tmp;
            i++;
        }
        node.next.next = curr; //
        node.next = prev;
        return fakeHead.next;
    }
}
```
```
Runtime
73 ms
Beats
89.27%
Memory
38.4 MB
Beats
53.66%
```