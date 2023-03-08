# Merge Two Sorted Lists

[题目](https://leetcode.com/problems/merge-two-sorted-lists/)

这题是合并两个已排序的列表。本来想着不难，最多实现丑陋一点。结果再仔细一看，不是列表，是单向列表，题目自己定义的。然后就有点难受，也不是说不能写，就是会很难看，程序内部需要判断是否为null的地方太多了。于是找到了一个比较简洁的算法，使用递归。

```c#
//这个定义我只放一次
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
    public ListNode MergeTwoLists(ListNode list1, ListNode list2) {
        if(list1==null) return list2;
        if(list2==null) return list1;
        if(list1.val<list2.val){
            list1.next=MergeTwoLists(list1.next,list2);
            return list1;
        }
        else{
            list2.next=MergeTwoLists(list1,list2.next);
            return list2;
        }
    }
}
```

```
Runtime
82 ms
Beats
88.77%
Memory
38.2 MB
Beats
89.54%
```

很容易想到的思路是创建一个res，然后判断list1和list2的值，谁小就把谁加进res。递归的做法是全程不创建新ListNode，就判断参数list1和list2，覆盖原有的next为更小的ListNode。一层一层往下覆盖，完成后返回到第一层，此时第一层的next已经完成全部排序了。不递归也行，就是下面这种：

```c#
public class Solution {
    public ListNode MergeTwoLists(ListNode list1, ListNode list2) {
        //If list1 is null means list2 is already sorted
        if(list1 == null){
            return list2;
        }
        //If list2 is null means list1 is already sorted
        if(list2 == null){
            return list1;
        }
        //Two Temporary variable to store the head of the goven linked list 
        
        ListNode t1 = list1;
        ListNode t2 = list2;

        //ansHead and ansTail will store answer list
        ListNode ansHead = null;
        ListNode ansTail = null;
         //to find the head of the answer linked list

        if(t1.val <= t2.val){
            //set head and tail
            ansHead = t1;
            ansTail = t1;
            t1 = t1.next;
        }
        else{
            //set head and tail
            ansHead = t2;
            ansTail = t2;
            t2 = t2.next;
        }
        while(t1 != null && t2 != null){

            if(t1.val <= t2.val){//if value in t1 is less than that of t2

            ansTail.next = t1;//add t1 node in answer tail
            ansTail = ansTail.next;//after adding new element the answer tail will move to next
            t1 = t1.next;//as you have visited the current t1 node move t1 to t1.next
            }
            else{

            ansTail.next = t2;//add t2 node in answer tail
            ansTail =ansTail.next;//after adding new element the answer tail will move to next
            t2 = t2.next;//as you have visited the current t1 node move t1 to t1.next
            }
        }

        //If one of the lis is empty then remaining list between t1 and t2 is alread sorted
        if(t1 != null){
            ansTail.next = t1;
        }
        else{
            ansTail.next = t2;
        }

        return ansHead;
    }
}
```

```
Runtime
90 ms
Beats
55.15%
Memory
38.7 MB
Beats
84.70%
```

这个解法没有递归优雅（？），表现也不是特别好。遍历做法就是根据val的大小，覆盖list1或list2为各自的next，然后继续比较，直到有一方为null。有一个为null后判断谁是null，next为不是null的那一方。因为这是引用赋值，所以在`ansHead = t1;ansTail = t1;`这个地方两者就已经同时指向t1（或者t2）了，这就是为啥后面一直在修改ansTail，却返回ansHead。ansHead的出现是为了解决最开始小的值被存入val而不是next的问题。