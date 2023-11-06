# [Find the Winner of an Array Game](https://leetcode.com/problems/find-the-winner-of-an-array-game)

我写的代码里总能透露出一种清澈的愚蠢
```c++
class Solution {
public:
    int getWinner(vector<int>& arr, int k) {
        if(k>=arr.size()) return *std::max_element(std::begin(arr), std::end(arr));
        int cur=arr[0];
        queue<int> q;
        for(int i=1;i<arr.size();i++){
            q.push(arr[i]);
        }
        int count=0;
        while(count<k){
            if(cur>q.front()){
                count++;
                q.push(q.front());
                q.pop();
            }
            else{
                q.push(cur);
                cur=q.front();
                q.pop();
                count=1;
            }
        }
        return cur;
    }
};
```
[editorial](https://leetcode.com/problems/find-the-winner-of-an-array-game/editorial)里有用queue和不用queue的做法。但是论不用queue，我还是更喜欢lee佬的超简洁代码：
```c++
//https://leetcode.com/problems/find-the-winner-of-an-array-game/solutions/768007/java-c-python-one-pass-o-1-space
class Solution {
public:
    int getWinner(vector<int>& A, int k) {
        int cur = A[0], win = 0;
        for (int i = 1; i < A.size(); ++i) {
            if (A[i] > cur) {
                cur = A[i];
                win = 0;
            }
            if (++win == k) break;
        }
        return cur;
    }
};
```
关键点在于我们只需要遍历vector一次。遍历一次后，要么有一个元素连续赢了k次，我们返回这个元素；要么当前的cur元素是最大元素。这时可以直接返回了，后续不会再有元素大于cur了