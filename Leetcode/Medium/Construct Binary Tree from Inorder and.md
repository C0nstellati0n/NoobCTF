# Construct Binary Tree from Inorder and Postorder Traversal

[题目](https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/description/)

我后序遍历的题都没写过你叫我写这题？不可能的，还是看大佬的吧。首先是递归做法。

```c#
/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     public int val;
 *     public TreeNode left;
 *     public TreeNode right;
 *     public TreeNode(int val=0, TreeNode left=null, TreeNode right=null) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
 //https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/solutions/3302159/easy-solutions-in-java-python-and-c-look-at-once/
public class Solution {
    public TreeNode BuildTree(int[] inorder, int[] postorder) {
        // Call the recursive function with full arrays and return the result
        return buildTree(inorder, 0, inorder.Length - 1, postorder, 0, postorder.Length - 1);
    }
    TreeNode buildTree(int[] inorder, int inStart, int inEnd, int[] postorder, int postStart, int postEnd) {
        // Base case
        if (inStart > inEnd || postStart > postEnd) {
            return null;
        }
        
        // Find the root node from the last element of postorder traversal
        int rootVal = postorder[postEnd];
        TreeNode root = new TreeNode(rootVal);
        
        // Find the index of the root node in inorder traversal
        int rootIndex = 0;
        for (int i = inStart; i <= inEnd; i++) {
            if (inorder[i] == rootVal) {
                rootIndex = i;
                break;
            }
        }
        
        // Recursively build the left and right subtrees
        int leftSize = rootIndex - inStart;
        int rightSize = inEnd - rootIndex;
        root.left = buildTree(inorder, inStart, rootIndex - 1, postorder, postStart, postStart + leftSize - 1);
        root.right = buildTree(inorder, rootIndex + 1, inEnd, postorder, postEnd - rightSize, postEnd - 1);
        
        return root;
    }
}
```

```
Runtime
87 ms
Beats
81.94%
Memory
40.2 MB
Beats
84.72%
```

然后是遍历做法。

```c#
 //https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/solutions/3302302/clean-codes-full-explanation-using-stack-c-java-python3/
public class Solution {
    public TreeNode BuildTree(int[] inorder, int[] postorder) {
        // If either of the input arrays are empty, the tree is empty, so return null
    if (inorder.Length == 0 || postorder.Length == 0) return null;
    
    // Initialize indices to the last elements of the inorder and postorder traversals
    int ip = inorder.Length - 1;
    int pp = postorder.Length - 1;

    // Create an empty stack to help us build the binary tree
    Stack<TreeNode> stack = new();
    // Initialize prev to null since we haven't processed any nodes yet
    TreeNode prev = null;
    // Create the root node using the last element in the postorder traversal
    TreeNode root = new TreeNode(postorder[pp]);
    // Push the root onto the stack and move to the next element in the postorder traversal
    stack.Push(root);
    pp--;

    // Process the rest of the nodes in the postorder traversal
    while (pp >= 0) {
        // While the stack is not empty and the top of the stack is the current inorder element
        while (stack.Count!=0 && stack.Peek().val == inorder[ip]) {
            // The top of the stack is the parent of the current node, so pop it off the stack and update prev
            prev = stack.Pop();
            ip--;
        }
        // Create a new node for the current postorder element
        TreeNode newNode = new TreeNode(postorder[pp]);
        // If prev is not null, the parent of the current node is prev, so attach the node as the left child of prev
        if (prev != null) {
            prev.left = newNode;
        // If prev is null, the parent of the current node is the current top of the stack, so attach the node as the right child of the current top of the stack
        } else if (stack.Count!=0) {
            TreeNode currTop = stack.Peek();
            currTop.right = newNode;
        }
        // Push the new node onto the stack, reset prev to null, and move to the next element in the postorder traversal
        stack.Push(newNode);
        prev = null;
        pp--;
    }

        // Return the root of the binary tree
        return root;
    }
}
```

```
Runtime
70 ms
Beats
100%
Memory
40.1 MB
Beats
84.72%
```

这道题需要从后序遍历入手。因为后序遍历是左右根的顺序，所以后序遍历的最后一个节点一定是最上面的根节点。这一步谁都看的出来，然后呢？回顾中序的左根右遍历，有没有发现什么？我们从后往前遍历后序，取到的节点是根节点。然后去中序遍历里找到这个节点的索引，它的左边就是左子树，右边就是右子树。左右子树又可以递归应用这套逻辑，直到左右子树大小为1时，递归返回。