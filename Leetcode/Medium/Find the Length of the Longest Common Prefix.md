# [Find the Length of the Longest Common Prefix](https://leetcode.com/problems/find-the-length-of-the-longest-common-prefix)

又是偷trie实现及其功能函数的一天
```c++
//采样区
// https://leetcode.com/problems/find-the-length-of-the-longest-common-prefix/editorial 的实现可能更好理解，但是这个更快
class TrieNode {
public:
    int data;
    TrieNode* children[10];
    bool isTerminal;
    TrieNode(int ch) {
        data = ch;
        for (int i = 0; i < 10; i++) { children[i] = NULL; }
        isTerminal = false;
    }
};
class Trie {
    TrieNode* root;
public:
    Trie() {
        root = new TrieNode(-1);
    }
    void insert(int data) {
        TrieNode* node = root;
        int divisor = 1;
        while (data / divisor >= 10) {
            divisor *= 10;
        }
        while (divisor > 0) {
            int digit = (data / divisor) % 10;
            if (node->children[digit] == NULL) {
                node->children[digit] = new TrieNode(digit);
            }
            node = node->children[digit];
            divisor /= 10;
        }
        node->isTerminal = true;
    }
    int prefixLen(int data) {
        TrieNode* node = root;
        int length = 0;
        int divisor = 1;
        while (data / divisor >= 10) { //这样搞就是从高位digit开始取
            divisor *= 10;
        }
        while (divisor > 0) {
            int digit = (data / divisor) % 10;
            if (node->children[digit] == NULL) {
                return length;
            }
            node = node->children[digit];
            length++;
            divisor /= 10; //然后逐步往低位digit走
        }
        return length;
    }
};
class Solution {
    Trie* trie = new Trie();
public:
    int longestCommonPrefix(vector<int>& arr1, vector<int>& arr2) {
        for (const int& num : arr1) {
            trie->insert(num);
        }
        int maxLen = 0;
        for (const int& num : arr2) {
            maxLen = max(trie->prefixLen(num), maxLen);
        }
        return maxLen;
    }
};
```