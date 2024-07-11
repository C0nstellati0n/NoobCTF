# [Reverse Substrings Between Each Pair of Parentheses](https://leetcode.com/problems/reverse-substrings-between-each-pair-of-parentheses)

等一下你说你叫什么名字？
```c++
//https://leetcode.com/problems/reverse-substrings-between-each-pair-of-parentheses/editorial
//如果有一天editorial收费了，见 https://leetcode.com/problems/reverse-substrings-between-each-pair-of-parentheses/solutions/383670/java-c-python-tenet-o-n-solution
class Solution {
public:
    string reverseParentheses(string s) {
        int n = s.length();
        stack<int> openParenthesesIndices;
        vector<int> pair(n);

        // First pass: Pair up parentheses
        for (int i = 0; i < n; ++i) {
            if (s[i] == '(') {
                openParenthesesIndices.push(i);
            }
            if (s[i] == ')') {
                int j = openParenthesesIndices.top();
                openParenthesesIndices.pop();
                pair[i] = j;
                pair[j] = i;
            }
        }

        // Second pass: Build the result string
        string result;
        for (int currIndex = 0, direction = 1; currIndex < n;
             currIndex += direction) {
            if (s[currIndex] == '(' || s[currIndex] == ')') {
                currIndex = pair[currIndex];
                direction = -direction;
            } else {
                result += s[currIndex];
            }
        }
        return result;
    }
};
```
真的是很巧妙的一个算法，还有点好玩（？）。关键是它叫Wormhole Teleportation technique，真的没见过这么高端的名字

至于它为什么能行……呃，我是这么想的。括号肯定是一层套一层的对吧，每一层括号意味着逆向一次里面的内容。第一次for循环我们先找到各层括号。遇到一个`(`就意味着要逆向内容了，于是找到对应的`)`，改变方向倒着走，等同于逆向里面的内容。这是要是再遇见一个`)`,说明里面嵌套的内容又逆向了一次，找到其对应的`(`换个方向继续遍历。这么遍历下去肯定能走过全部的字符

很适合脑算的一个算法，但不适合自己发明