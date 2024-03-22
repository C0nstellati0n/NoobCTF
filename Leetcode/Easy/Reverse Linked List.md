# [Reverse Linked List](https://leetcode.com/problems/reverse-linked-list)

之前见过对这里代码的引用，终于等到今天好好学习了
```c++
class Solution {
public:
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
说“好好学习”其实就是找个好的solution。[这个](https://leetcode.com/problems/reverse-linked-list/solutions/803955/c-iterative-vs-recursive-solutions-compared-and-explained-99-time-85-space)就不错，还有动图