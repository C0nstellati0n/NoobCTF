# [Greatest Common Divisor Traversal](https://leetcode.com/problems/greatest-common-divisor-traversal)

啊？
```c++
//采样区
//原本有siz数组，个人发现这道题没用便删除了
const int mex = 1e5 + 5;
int par[mex];
int A[mex];
void init(int x) //初始化质数列表
{
    for (int i = 0; i <= x; ++i)
    {
        par[i] = i; //顺便把union find的数据结构初始了
        A[i] = 0;
    }
    for (int i = 2; i <= x; ++i)
    {
        if (A[i] == 0) //若A[i]为0，说明当前的i为质数
        {
            A[i] = i;
            for (int j = 2 * i; j <= x; j += i) //划掉所有当前质数i的倍数
            {
                A[j] = i; //这里感觉记录的是“数字j的最大质数因子”。考虑2和3，两者的倍数都有6，最后A[6]的值为3，即为6的最大质数因子
            }
        }
    }
}
int finder(int x)
{
    if (x == par[x]) return x;
    return par[x] = finder(par[x]);
}
void merge(int a, int b)
{
    int x1 = finder(a);
    int x2 = finder(b);
    if (x1 != x2)
    {
        par[x2] = x1;
    }
}
class Solution
{
    public:
        bool canTraverseAllPairs(vector<int> &v)
        {
            int x = 0;
            if(v.size()==1)
                return true;
            for (auto i: v)
            {
                if (i == 1) return false;
                x = max(x, i);
            }
            init(x); //x是数组v里最大的数字，为初始化时的上限
            for (auto i: v)
            {
                int x = i;
                while (x > 1)
                {
                    int p = A[x];
                    merge(i, p); //将当前数字i与其对应的质数连接起来
                    while (x % p == 0 && x > 1) //获取质数分解
                        x /= p;
                }
            }
            int f = finder(v[0]);
            for (auto i: v)
                if (finder(i) != f)
                    return false;
            return true;
        }
};
```
采样区永远有神人