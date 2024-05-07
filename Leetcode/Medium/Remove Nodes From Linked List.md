# [Remove Nodes From Linked List](https://leetcode.com/problems/remove-nodes-from-linked-list)

会monotonic stack但不会倒着组装linked list的我……
```c++
//参考了 https://leetcode.com/problems/remove-nodes-from-linked-list/solutions/5118366/detailed-explanation-3-approaches-stack-recursion-reversal-o-1-space-efficient
class Solution {
public:
    ListNode* removeNodes(ListNode* head) {
        stack<ListNode*> s;
        while(head){
            while(!s.empty()&&s.top()->val<head->val){
                s.pop();
            }
            s.push(head);
            head=head->next;
        }
        ListNode* ans=nullptr; //一定要将其初始化为nullptr，不然报错
        while(!s.empty()){ //最后面的node在最上面，所以要倒着组装
            head=s.top();
            s.pop();
            head->next=ans;
            ans=head;
        }
        return ans;
    }
};
```
[editorial](https://leetcode.com/problems/remove-nodes-from-linked-list/editorial)还有递归和反转list做法