# Split Linked List in Parts

[题目](https://leetcode.com/problems/split-linked-list-in-parts/description)

明明我们看的是同一个hint，想的是同一个思路，为什么我的代码看起来就那么垃圾？
```c#
//https://leetcode.com/problems/split-linked-list-in-parts/solutions/4007634/95-full-explanation-beginner-friendly-two-pass-method/ 的讲解似乎更详细
public class Solution {
    public ListNode[] SplitListToParts(ListNode head, int k) {
        ListNode[] res=new ListNode[k];
        ListNode copy=head;
        int count=0;
        while(copy!=null){
            count++;
            copy=copy.next;
        }
        int partCount=count/k;
        int extra=count%k;
        ListNode previous=null;
        int totalCount;
        for(int i=0;i<k;i++){
            if(i<extra){
                totalCount=partCount+1;
            }
            else{
                totalCount=partCount;
            }
            copy=head;
            for(int j=0;head!=null&&j<totalCount;j++){
                previous=head;
                head=head.next;
            }
            if(copy!=null){
                previous.next=null;
            }
            res[i]=copy;
        }
        return res;
    }
}
```
```
Runtime
109 ms
Beats
100%
Memory
43.9 MB
Beats
23.8%
```
[editorial](https://leetcode.com/problems/split-linked-list-in-parts/editorial)有个不分割list而是创建新list的。当然space没有split的做法好。