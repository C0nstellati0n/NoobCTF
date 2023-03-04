# Remove Duplicates from Sorted List

[题目](https://leetcode.com/problems/remove-duplicates-from-sorted-list/description/)

从已排序的单向链表中移除重复元素。不是第一次遇见单向链表了，所以稍微有点思路。但是我有点搞不清引用赋值和值赋值，把链表搞乱了。其实代码非常简单：

```c#
/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     public int val;
 *     public ListNode next;
 *     public ListNode(int val=0, ListNode next=null) {
 *         this.val = val;
 *         this.next = next;
 *     }
 * }
 */
public class Solution {
    public ListNode DeleteDuplicates(ListNode head) {
        ListNode curr=head;
        while (curr!=null){
            while (curr.next!=null && curr.val==curr.next.val) curr.next=curr.next.next;
            curr=curr.next;
        }
        return head;
    }
}
```

```
Runtime
80 ms
Beats
94.74%
Memory
40.2 MB
Beats
16.67%
```

这里的curr是head的引用拷贝，它们指向同一块内存。while循环里通过将curr.next.next覆盖curr.next（重复的）来去除重复值。最后返回head就好了，因为修改curr其实就是在修改head。