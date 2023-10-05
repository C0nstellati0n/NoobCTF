# [Design HashMap](https://leetcode.com/problems/design-hashmap)

我要裂开了。
```c#
class MyHashMap {
    int[] data;
    public MyHashMap() {
        data = new int[1000001];
        Array.Fill(data, -1);
    }
    public void Put(int key, int val) {
        data[key] = val;
    }
    public int Get(int key) {
        return data[key];
    }
    public void Remove(int key) {
        data[key] = -1;
    }
}
```
```
Runtime
206 ms
Beats
95.16%
Memory
56.5 MB
Beats
75.40%
```
道心破碎，这回真的碎了一地。我的想法也差不多，毕竟constraint里说key和value不超过1e6，那就直接搞个这么长的数组即可。我看错了，看成下面的1e4了。还有个难一点的用listnode的做法。
```c#
//采样区
//思路和 https://leetcode.com/problems/design-hashmap/solutions/1097755/js-python-java-c-updated-hash-array-solutions-w-explanation 差不多，但是快了很多，内存多了
public class MyHashMap {
    class LNode
    {
        public int key {get; set;}
       public int val {get; set;}
       public LNode next {get; set;} = null;      
    }
    LNode[] lnarr;
    public MyHashMap() {
        lnarr = new LNode[1000];
    }
    public void Put(int key, int value) {
       var ih = hash(key);
        if(lnarr[ih] == null)
        {
            lnarr[ih] = new LNode()
            {
              key = key,
                val = value
            };

            return;
        }
        var ln = lnarr[ih];
        LNode prev = null;
        while(ln != null)
        {
            if(ln.key == key)
            {
                ln.val = value;
                return;
            }
            if(ln.next == null)
            {
                prev = ln;
                break;
            }
            ln = ln.next;
        }
        prev.next = new LNode()
        {
          key = key,
            val = value
        };
    }
    public int Get(int key) {
       int ih = hash(key);
        var ln = lnarr[ih];
        while(ln != null)
        {
            if(ln.key == key)
                return ln.val;
            
            ln = ln.next;
        }
        return -1;
    }
    public void Remove(int key) {
        int ih = hash(key);
        if(lnarr[ih] == null)
            return;
        else if(lnarr[ih].key == key)
        {
            lnarr[ih] = lnarr[ih].next;
            return;
        }
        var ln = lnarr[ih];
        while(ln.next != null)
        {
            if(ln.next.key == key)
            {
                ln.next = ln.next.next;
                return;
            }
            ln = ln.next;
        }
    }
    private int hash(int key) => key % 1000;
}
```
```
Runtime
183 ms
Beats
100%
Memory
123.3 MB
Beats
16.94%
```