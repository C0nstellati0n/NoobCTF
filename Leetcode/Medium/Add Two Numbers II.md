# Add Two Numbers II

[题目](https://leetcode.com/problems/add-two-numbers-ii/description/)

逻辑是很简单的，就是写的怎么这么别扭啊？
```c#
public class Solution {
    public ListNode AddTwoNumbers(ListNode l1, ListNode l2) {
        Stack<int> s1=new();
        Stack<int> s2=new();
        while(l1!=null){
            s1.Push(l1.val);
            l1=l1.next;
        }
        while(l2!=null){
            s2.Push(l2.val);
            l2=l2.next;
        }
        List<int> res=new();
        int num1,num2;
        int over=0;
        int cur=0;
        while(s1.Any()||s2.Any()||over!=0){
            num1=0;
            num2=0;
            if(s1.Any()){
                num1=s1.Pop();
            }
            if(s2.Any()){
                num2=s2.Pop();
            }
            cur=(num1+num2+over)%10;
            over=(num1+num2+over)/10;
            res.Add(cur);
        }
        ListNode ans=new();
        ListNode copy=ans;
        for(int i=res.Count-1;i>=1;i--){
            ans.val=res[i];
            ans.next=new();
            ans=ans.next;
        }
        ans.val=res[0];
        return copy;
    }
}
```
```
Runtime
90 ms
Beats
95.5%
Memory
50.6 MB
Beats
13.86%
```
也可以不用stack，通过反转linked list来达到同样的效果。参考[editorial](https://leetcode.com/problems/add-two-numbers-ii/editorial/)