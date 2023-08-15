# Partition List

[题目](https://leetcode.com/problems/partition-list/description/)

我在写什么？写了半天写出解构主义了是吧？
```c#
public class Solution {
    public ListNode Partition(ListNode head, int x) {
        if(head==null){
            return null;
        }
        List<ListNode> smallerNodes=new();
        List<ListNode> greaterEqualNodes=new();
        while(head!=null){
            if(head.val<x){
                smallerNodes.Add(head);
            }
            else{
                greaterEqualNodes.Add(head);
            }
            head=head.next;
        }
        ListNode res=new();
        ListNode copy=res;
        bool flag=false;
        if(smallerNodes.Count>=1){
            res.val=smallerNodes[0].val;
            flag=true;
        }
        for(int i=1;i<smallerNodes.Count;i++){
            res.next=new();
            res=res.next;
            res.val=smallerNodes[i].val;
        }
        if(greaterEqualNodes.Count>=1){
            if(flag){
                res.next=new();
                res=res.next;
            }
            res.val=greaterEqualNodes[0].val;
        }
        for(int i=1;i<greaterEqualNodes.Count;i++){
            res.next=new();
            res=res.next;
            res.val=greaterEqualNodes[i].val;
        }
        return copy;
    }
}
```
```
Runtime
75 ms
Beats
88.66%
Memory
39.2 MB
Beats
35.57%
```
对你没看错，真就是写了这么长。这题要是用two pointers会好很多。 https://leetcode.com/problems/partition-list/solutions/29185/very-concise-one-pass-solution/