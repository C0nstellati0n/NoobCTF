# Maximum Twin Sum of a Linked List

[题目](https://leetcode.com/problems/maximum-twin-sum-of-a-linked-list/description/)

本来想挑战一下discussion里面提到的space O(1)的解法的。结果space缩减了，time直接tle了。还是用我的trivial解法吧。

```c#
public class Solution {
    public int PairSum(ListNode head) {
        int n=0;
        int max=0;
        List<int> nums=new();
        while(head!=null){
            nums.Add(head.val);
            head=head.next;
            n++;
        }
        for(int i=0;i<=n/2-1;i++){
            max=Math.Max(max,nums[i]+nums[n-1-i]);
        }
        return max;
    }
}
```
```
Runtime
271 ms
Beats
85.84%
Memory
55.3 MB
Beats
76.99%
```
优化解法如下。
```c#
//https://leetcode.com/problems/maximum-twin-sum-of-a-linked-list/solutions/1680417/c-python-mid-and-reverse-solution/
public class Solution {
    public int PairSum(ListNode head) {
        ListNode slow = head;
        ListNode fast = head;
        int maxVal = 0;

        // Get middle of linked list
        while(fast!=null && fast.next!=null) //如果是我来写这个解法的话，我只能想到让一个指针到linked list的中央，一个在头部。然后就没有然后了，不懂了。原来可以让两个指针一个在中央，一个在末尾，然后从中央那个指针开始，反转后面的。至于怎么让指针到中央，我想的是先while一下数node，然后for到中央。如果像大佬这么实现的话，省了一个循环
        {
            fast = fast.next.next;
            slow = slow.next;
        }

        // Reverse second part of linked list
        ListNode nextNode, prev = null;
        while (slow!=null) {
            nextNode = slow.next;
            slow.next = prev;
            prev = slow;
            slow = nextNode;
        }
        // Get max sum of pairs
        while(prev!=null)
        {
            maxVal = Math.Max(maxVal, head.val + prev.val);
            prev = prev.next; //交换node就是为了解决单向链表没法往回走的问题。现在直接无脑next就是题目想要的pair了
            head = head.next;
        }
        return maxVal;
    }
}
```
```
Runtime
240 ms
Beats
100%
Memory
57.5 MB
Beats
26.55%
```