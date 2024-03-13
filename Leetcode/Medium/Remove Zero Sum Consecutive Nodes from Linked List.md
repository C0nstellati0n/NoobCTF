# [Remove Zero Sum Consecutive Nodes from Linked List](https://leetcode.com/problems/remove-zero-sum-consecutive-nodes-from-linked-list)

糟了把单向链表忘了。让[editorial](https://leetcode.com/problems/remove-zero-sum-consecutive-nodes-from-linked-list/editorial)捞捞我
```c++
class Solution {
public:
    ListNode* removeZeroSumSublists(ListNode* head) {
        ListNode* front = new ListNode(0, head);
        ListNode* current = front;
        int prefixSum = 0;
        unordered_map<int, ListNode*> prefixSumToNode;
        while (current != nullptr) {
            // Add current's value to the prefix sum
            prefixSum += current->val;
            // If prefixSum is already in the hashmap, 
            // we have found a zero-sum sequence:
            if (prefixSumToNode.find(prefixSum) != prefixSumToNode.end()) {
                ListNode* prev = prefixSumToNode[prefixSum];
                current = prev->next;
                // Delete zero sum nodes from hashmap
                // to prevent incorrect deletions from linked list
                int p = prefixSum + current->val;
                while (p != prefixSum) {
                    prefixSumToNode.erase(p);
                    current = current->next;
                    p += current->val;
                }
                // Make connection from the node before 
                // the zero sum sequence to the node after
                prev->next = current->next;
            } else {
                // Add new prefixSum to hashmap
                prefixSumToNode[prefixSum] = current;
            }
            // Progress to next element in list
            current = current->next;
        }
        return front->next;
    }
};
```
这题的一个关键点在于Consecutive，要求删除和为0的连续node。我们用map记录prefix sum，若某个prefix sum在map里出现过，说明那个出现过的prefix sum对应的node与当前node之间的全部node和为0，可以删除。至于删除的方式，我只能说单向链表真的烦，在这里记一遍以后就可以直接抄了！