# [K-th Smallest in Lexicographical Order](https://leetcode.com/problems/k-th-smallest-in-lexicographical-order)

直接上editorial吧，太菜了
```c++
//https://leetcode.com/problems/k-th-smallest-in-lexicographical-order/editorial
class Solution {
public:
    int findKthNumber(int n, int k) {
        int curr = 1;
        k--;
        while (k > 0) {
            int step = countSteps(n, curr, curr + 1);
            if (step <= k) { //两个prefix之间的node数量小于k，直接跳过
                curr++;
                k -= step;
            } else { //k在两个prefix的node之间
                curr *= 10; //往下降一层，沿着子树往下走
                k--;
            }
        }
        return curr;
    }
private:
    int countSteps(int n, long prefix1, long prefix2) {
        int steps = 0;
        while (prefix1 <= n) {
            steps += min((long)(n + 1), prefix2) - prefix1;
            prefix1 *= 10;
            prefix2 *= 10;
        }
        return steps;
    }
};
```
这题有个prefix tree的概念（广义的，不一定非要实现一个trie类），值得记录一下。个人觉得难理解的是countSteps函数，怎么计算prefix tree中两个prefix中间隔的node的数量？这里建议看discussion区tsuvmxwu的评论配合 http://bookshadow.com/weblog/2016/10/24/leetcode-k-th-smallest-in-lexicographical-order/ 里给出的例子理解