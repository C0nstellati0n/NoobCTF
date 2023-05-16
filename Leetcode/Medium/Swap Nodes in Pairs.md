# Swap Nodes in Pairs

[题目](https://leetcode.com/problems/swap-nodes-in-pairs/)

昨天说linked list难不住我了，今天看来我说早了。或许linked list难不住我，但是引用之间的赋值够我吃一壶了。

```c#
//https://leetcode.com/problems/swap-nodes-in-pairs/solutions/1775033/swapping-nodes-not-just-the-values-visual-explanation-well-explained-c/
public class Solution {
    public ListNode SwapPairs(ListNode head) {
        if(head==null || head.next==null) return head; //If there are less than 2 nodes in the given nodes, then no need to do anything just return the list as it is.
		
        ListNode dummyNode = new ListNode();
        
        ListNode prevNode=dummyNode; //由于引用赋值，prevNode就是dummyNode。dummyNode只是为了最后返回用的
        ListNode currNode=head;
        
        while(currNode!=null && currNode.next!=null){
            prevNode.next = currNode.next;
            currNode.next = prevNode.next.next; //结合上面就是currNode.next=currNode.next.next
            prevNode.next.next = currNode; //currNode.next.next=currNode
            //以上是交换逻辑
            prevNode = currNode; //node往下移
            currNode = currNode.next;
        }
        
        return dummyNode.next; //dummyNode本身没有值，根据上面的逻辑，dummyNode.next才是交换后的head
    }
}
```

```
Runtime
81 ms
Beats
82.9%
Memory
38.1 MB
Beats
61.15%
```

递归解法。

```c#
//https://leetcode.com/problems/swap-nodes-in-pairs/solutions/1774708/c-visual-image-how-links-change-explained-every-step-commented-code/
public class Solution {
    public ListNode SwapPairs(ListNode head) {
        // if head is null OR just having a single node, then no need to change anything 
        if(head == null || head . next == null) 
        {
            return head;
        }
            
        ListNode temp; // temporary pointer to store head . next
        temp = head.next; // give temp what he want
        
        head.next = SwapPairs(head.next.next); // changing links
        temp.next = head; // put temp . next to head
        
        return temp; // now after changing links, temp act as our head
    }
}
```

```
Runtime
74 ms
Beats
94.43%
Memory
38 MB
Beats
61.15%
```