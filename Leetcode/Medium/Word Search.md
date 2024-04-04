# [Word Search](https://leetcode.com/problems/word-search)

瞄了一眼题目描述就高高兴兴地写了个多源bfs。然后发现不能用。再一看discussion区和constraint，什么这是个backtrack+dfs？
```c++
//采样区
class Solution {
public:
    bool exist(vector<vector<char>>& board, string word) {
        if(count(word.begin(), word.end(), word[0]) > count(word.begin(), word.end(), word[word.size()-1])) 
            reverse(word.begin(), word.end());
        for (int i = 0; i < board.size(); i++) {
            for (int j = 0; j < board[0].size(); j++) {
                if (check(board, word, i, j, 0))
                    return true;
            }
        }
        return false;
    }
    bool check(vector<vector<char>>& board, string& word, int i, int j, int k) {
        if (k == word.size())
            return true;
        if (i<0 || i>=board.size() || j<0 || j>=board[0].size() || board[i][j] != word[k]) {
            return false;
        }
        char c = board[i][j];
        board[i][j] = '*';
        bool found = check(board, word, i - 1, j, k + 1) || check(board, word, i, j + 1, k + 1) || check(board, word, i + 1, j, k + 1) || check(board, word, i, j - 1, k + 1);
        board[i][j] = c;
        return found;
    }
};
```
永远要感叹采样区牛逼。开头那段反转word的做法作用是提速。不加这句也能过，但是加上后速度快了10倍……稍微能猜到一点为什么。到底要dfs+backtrack多少次取决于word的开头第一个字符。那既然尾部的字符数量比头部的少，就可以反转word，执行更少次数的backtrack自然就更快了

剩下的就是标准backtrack（mark，操作后再unmark），dfs遍历上下左右所有可能路径。至于bfs为啥不可以，我想是因为bfs本质上先考虑广度，一圈一圈地往外扩张，没法一条路走到黑，和backtrack的爆破配合不好