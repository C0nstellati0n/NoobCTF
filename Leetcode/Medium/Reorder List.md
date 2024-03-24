# [Reorder List](https://leetcode.com/problems/reorder-list)

三十分钟前：不就是用fast&slow pointer找到中段再逆向后面那段再把它合在一起吗？前两个都学过了，最后一个还能出问题？

三十分钟后：能
```c++
//https://leetcode.com/problems/reorder-list/solutions/1641006/c-python-simple-solutions-w-explanation-2-pointers-o-n-inplace-o-1-space-approaches
class Solution {
public:
    void reorderList(ListNode* head) {
        if(!head || !head -> next) return;
        ListNode* fast=head;
        ListNode* slow=head;
        while(fast&&fast->next){
            fast=fast->next->next;
            slow=slow->next;
        }
        ListNode* R = reverseList(slow);
        ListNode* L = head -> next;
        for(int i = 0; L != R; i++, head = head -> next){
            if(i & 1) {                              
                head -> next = L;
                L = L -> next;
            }
            else {
                head -> next = R;
                R = R -> next;
            }
        }
    }
    ListNode* reverseList(ListNode* head) {
        ListNode* prev=NULL;
        ListNode* follow=NULL;
        while (head)
        {
            follow = head->next;
            head->next = prev;
            prev = head;
            head = follow;
        }
        return prev;
    }
};
```
但当时自己尝试时用的不是for循环，是想要下面的效果：
```c++
class Solution {
public:
    void reorderList(ListNode* head) {
        ListNode* slow = head;
        ListNode* fast = head;
        while (fast != nullptr && fast->next != nullptr)
        {
            slow = slow->next;
            fast = fast->next->next;
        }
        ListNode* mid = slow->next;
        slow->next = nullptr;
        ListNode* prev = nullptr;
        for (ListNode* current = mid; current != nullptr ;)
        {
            ListNode* tmp = current->next;
            current->next = prev;
            prev = current;
            current = tmp;
        }
        ListNode *current = head;
        while (prev != nullptr)
        {
            //自己写的时候只想到用一个temp，废物
            ListNode* tmp1 = current->next;
            ListNode* tmp2 = prev->next;
            current->next = prev;
            prev->next = tmp1;
            prev = tmp2;
            current = current->next->next;
        }
    }
};
```