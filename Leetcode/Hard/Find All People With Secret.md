# [Find All People With Secret](https://leetcode.com/problems/find-all-people-with-secret)

失之毫厘，差之千里：一个小细节不会整个题都不会
```c++
//采样区
//个人觉得editorial的unionFind解法更好理解点，还有动图
class UnionFindSet
{
public:
    UnionFindSet(int n) : _parent(n), _size(n)
    {
        for(int i = 0; i < n; ++i)
        {
            _parent[i] = i;
            _size[i] = 1;
        }
    }
    bool Union(int x, int y)
    {
        int rootX = Find(x);
        int rootY = Find(y);
        if(rootX == rootY)
        {
            return true;
        }
        if(rootX != rootY)
        {
            if(_size[rootY] < _size[rootX])
            {
                _parent[rootY] = rootX;
                _size[rootX] += _size[rootY];
            }
            else
            {
                _parent[rootX] = rootY;
                _size[rootY] += _size[rootX];
            }
        }
        return false;
    }

    int Find(int x)
    {
        if(_parent[x] == x)
        {
            return x;
        }
        return _parent[x] = Find(_parent[x]);
    }

    int getGroup()
    {
        int g = 0;
        for(int i = 0; i < _parent.size(); ++i)
        {
            if(i == _parent[i])
            {
                ++g;
            }
        }
        return g;
    }
    vector<int> getGroupVec()
    {
        vector<int> res;
        for(int i = 0; i < _parent.size(); ++i)
        {
            if(_parent[0] == _parent[i])
            {
                res.emplace_back(i);
            }
        }
        return res;
    }
    void set(int num)
    {
        _parent[num] = num;
        _size[num] = 1;
    }
private:
    vector<int> _parent;
    vector<int> _size;
};
class Solution
{
public:
    vector<int> findAllPeople(int n, vector<vector<int>> &meetings, int firstPerson)
    {
        sort(meetings.begin(), meetings.end(), [&](vector<int> &a, vector<int> &b)
            {
                return a[2] < b[2];
            });
        vector<int> res(1, 0);
        UnionFindSet ufs(n);
        ufs.Union(0, firstPerson);
        int m = meetings.size();
        for(int i = 0; i < m; ++i)
        {
            int time = meetings[i][2];
            ufs.Union(meetings[i][0], meetings[i][1]);
            //我觉得整道题这里是重点。union类抄之前见过的就完事，for循环前都是些基本设置，只有这个if解决了困扰我的问题
            //单纯遍历meetings一遍，把node union起来，最后检查是否与node 0连着有个问题：假如此时是时间1，node 3和node 4连接起来；时间2时node 4得知了secret，与node 0连起来，但是node 3明明不知道secret（node 4在时间1时不知道secret，没法告诉node 3），却因为与node 4连接起来而间接与node 0连接起来，与题目描述不符
            if(i == m - 1 || meetings[i][2] != meetings[i + 1][2]) //所以当时间往前进了一步 （meetings[i][2] != meetings[i + 1][2]），或是已经是最后meeting时（i == m - 1），要检查meeting连接起来的node是否与node 0连着。若连着则没事，若不连着则断开（ufs.set），此时的断开操作不会影响之前的连通性
            {
                int j = i;
                while(j >= 0 && meetings[j][2] == time)
                {
                    if(ufs.Find(meetings[j][1]) != ufs.Find(0))
                    {
                        ufs.set(meetings[j][1]);
                    }
                    if(ufs.Find(meetings[j][0]) != ufs.Find(0))
                    {
                        ufs.set(meetings[j][0]);
                    }
                    --j;
                }
            }
        }
        return ufs.getGroupVec();
    }
};
```
这个做法相比于editorial，用if语句优化了检查meeting的次数。除此之外，editorial还有bfs/dfs解法，相比于以往的bfs/dfs，多了个时间方面的考量。我怎么觉得union find解法更好理解一点？