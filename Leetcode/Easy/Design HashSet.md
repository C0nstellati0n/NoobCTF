# Design HashSet

[题目](https://leetcode.com/problems/design-hashset/description/)

又是简单的快乐。

```c#
public class MyHashSet {
    List<int> hashSet;
    public MyHashSet() {
        hashSet=new();
    }
    
    public void Add(int key) {
        if(!hashSet.Contains(key))
            hashSet.Add(key);
    }
    
    public void Remove(int key) {
        if(hashSet.Contains(key))
            hashSet.Remove(key);
    }
    
    public bool Contains(int key) {
        return hashSet.Contains(key);
    }
}
```
```
Runtime
260 ms
Beats
28.95%
Memory
66.5 MB
Beats
53.29%
```
魔法位运算解法。
```c#
//https://leetcode.com/problems/design-hashset/solutions/769047/java-solution-using-bit-manipulation/
public class MyHashSet {
    int[] num;
    public MyHashSet() {
        num = new int[31251];
    }
	
	// set the bit if that element is present
    public void Add(int key) {
        num[getIdx(key)]|=getMask(key);
    }
	
	//unset the bit if a key is not present
    public void Remove(int key) {
        num[getIdx(key)] &= (~getMask(key));
    }
	
	//check if bit corresponding to the key is set or not
    public bool Contains(int key) {
        return (num[getIdx(key)]&getMask(key))!=0;
    }
	
	// idx of num[] to which this key belongs
	// for key = 37, it will give 1
    private int getIdx(int key)
    {
        return (key/32);
    }
	
	// get mask representing the bit inside num[idx] that corresponds to given key.
	// for key = 37, it will give 00000000000000000000000000100000
    private int getMask(int key)
    {
        key%=32;
        return (1<<key);
    }
}
```
```
Runtime
203 ms
Beats
97.37%
Memory
62 MB
Beats
98.3%
```
偷懒继承写法（记下来纯粹是图一乐，肯定是不能这么写的）
```c#
//https://leetcode.com/problems/design-hashset/solutions/1621844/the-one-liner-solution-that-you-should-not-give/
public class MyHashSet:HashSet<int> {
}
```
```
Runtime
216 ms
Beats
89.47%
Memory
66.6 MB
Beats
53.29%
```