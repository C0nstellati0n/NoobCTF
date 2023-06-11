# Snapshot Array

[题目](https://leetcode.com/problems/snapshot-array/description/)

第一次做题逻辑会写，但是超内存。结果到最后也没做出来。
```c#
//https://leetcode.com/problems/snapshot-array/solutions/350562/java-python-binary-search/
public class SnapshotArray {
    SortedDictionary<int, int>[] A;
    int snap_id = 0;
    public SnapshotArray(int length) {
        A = new SortedDictionary<int,int>[length];
        for (int i = 0; i < length; i++) {
            A[i] = new SortedDictionary<int, int>();
            A[i][0]=0;
        }
    }

    public void Set(int index, int val) {
        A[index][snap_id]=val;
    }

    public int Snap() {
        return snap_id++;
    }

    public int Get(int index, int snap_id) {
        SortedDictionary<int, int> temp=A[index];
        while(!temp.ContainsKey(snap_id)){ //原解法是java的floorEntry，这里应该用binary search替代。原解法很快的
            snap_id--;
        }
        return A[index][snap_id];
    }
}
```
```
Runtime
2674 ms
Beats
5%
Memory
104.5 MB
Beats
92.50%
```
应该像下面这么写才对。
```c#
public class SnapshotArray {
    private int _snapId;
    private Dictionary<int, List<(int id, int value)>> _history; //似乎是KeyValuePair的list？

    public SnapshotArray(int length) {
        _history = new Dictionary<int, List<(int id, int value)>>();

        for (int i = 0; i < length; i++){
            _history[i] = new List<(int id, int value)>();
            _history[i].Add((0, 0));
        }
    }
    
    public void Set(int index, int val) {
        _history[index].Add((_snapId, val));
    }
    
    public int Snap() {
        return _snapId++;
    }
    
    public int Get(int index, int snap_id) {
        int left = 0;
        int right = _history[index].Count - 1;

        while (left <= right){
            int mid = left + (right - left) / 2;

            if (_history[index][mid].id <= snap_id){
                left = mid + 1;
            }
            else{
                right = mid - 1;
            }
        }
        return _history[index][right].value;
    }
}
```
```
Runtime
622 ms
Beats
100%
Memory
100.8 MB
Beats
95%
```