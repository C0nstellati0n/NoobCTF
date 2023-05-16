# Swapping Nodes in a Linked List

[题目](https://leetcode.com/problems/swapping-nodes-in-a-linked-list/description/)

linked list已经难不住我了！

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
    public ListNode SwapNodes(ListNode head, int k) {
        int count=k;
        ListNode first;
        ListNode back=head;
        ListNode copy=head;
        for(int i=1;i<k;i++){
            head=head.next;
        }
        first=head;
        while(head.next!=null){
            head=head.next;
            count++;
        }
        for(int i=1;i<=count-k;i++){
            back=back.next;
        }
        int temp=first.val;
        first.val=back.val;
        back.val=temp;
        return copy;
    }
}
```

```
Runtime
262 ms
Beats
73.26%
Memory
60.8 MB
Beats
10.47%
```

提交的时候我感觉我的解法有地方是多余的，但是又不会改。看看大佬们的解法。

```c#
//https://leetcode.com/problems/swapping-nodes-in-a-linked-list/solutions/1009800/c-j-p3-one-pass/
public class Solution {
    public ListNode SwapNodes(ListNode head, int k) {
        ListNode n1 = null, n2 = null;
        for (var p = head; p != null; p = p.next) { //这个用for循环遍历linked list还是挺巧妙的
            n2 = n2 == null ? null : n2.next;
            if (--k == 0) { //这里很巧妙的一点是，当--k==0时，正好是前面那个n1的停止处。如果在这里让后面的n2开始遍历，刚好会停在倒着数第k个处
                n1 = p;
                n2 = head;
            }
        }
        // The problem description specifically asks to swap values, not nodes themselves. 
        int tmp = n1.val;
        n1.val = n2.val;
        n2.val = tmp;
        return head;
    }
}
```

```
Runtime
251 ms
Beats
95.35%
Memory
60.4 MB
Beats
52.33%
```

我的解法和下面这个比较像。看来我是多了个for循环。

```c#
//https://leetcode.com/problems/swapping-nodes-in-a-linked-list/solutions/1009918/java-two-pointers-detailed-explanation-o-n-time-o-1-space/
class Solution {
    public ListNode SwapNodes(ListNode head, int k) {		
        ListNode fast = head;
        ListNode slow = head;
        ListNode first = head, second = head;
        
		// Put fast (k-1) nodes after slow
        for(int i = 0; i < k - 1; ++i)
            fast = fast.next;
            
		// Save the node for swapping
        first = fast;

		// Move until the end of the list
        while(fast.next != null) {
			slow = slow.next;
            fast = fast.next;
        }
        
        // Save the second node for swapping
		// Note that the pointer second isn't necessary: we could use slow for swapping as well
		// However, having second improves readability
        second = slow;
		
		// Swap values
        int temp = first.val;
        first.val = second.val;
        second.val = temp;
        
        return head;
    }
}
```
```
Runtime
265 ms
Beats
68.60%
Memory
60.8 MB
Beats
10.47%
```