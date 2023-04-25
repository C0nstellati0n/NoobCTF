# Smallest Number in Infinite Set

[题目](https://leetcode.com/problems/smallest-number-in-infinite-set/description/)

能在极短的时间里一下就找到用时内存均最差的解法也是有点本事的。

```c#
public class SmallestInfiniteSet {
    int smallest=1;
    List<int> numbers=Enumerable.Range(1, 1000).ToList();
    List<int> numbersNotIn=new();
    public SmallestInfiniteSet() {
        
    }
    
    public int PopSmallest() {
        smallest=numbers.Where(num=>!numbersNotIn.Contains(num)).Min();
        numbersNotIn.Add(smallest);
        return smallest;
    }
    
    public void AddBack(int num) {
        if(numbersNotIn.Contains(num)){
            numbersNotIn.Remove(num);
        }
        if(num<smallest){
            smallest=num;
        }
    }
}
```

```
Runtime
3916 ms
Beats
8%
Memory
58.3 MB
Beats
20%
```

差的地方在于每次都用Linq去查询，这样操作怎么可能不慢。这题虽说是“无限数字序列”，其实num的大小不会超过1000，这才有了一个numbers列表。其实不要也照样能做。

```c#
public class SmallestInfiniteSet {
    SortedSet<int> heap;
    int currentVal = 1; //目前最小的数字

    public SmallestInfiniteSet() {
        heap = new SortedSet<int>();
    }
    
    public int PopSmallest() {
        if(heap.Count > 0) //heap里有数字说明之前添加过比currentVal小的数字
        {
            int min = heap.Min;
            heap.Remove(min);
            return min;
        }
        return currentVal++; //没添加过currentVal就是最小的，返回后自增
    }
    
    public void AddBack(int num) {
        if(currentVal > num) //heap只记录比当前num小的数字
            heap.Add(num);
    }
}
```

```
Runtime
145 ms
Beats
100%
Memory
57.3 MB
Beats
44%
```

关键点在于意识到调用AddBack时，如果添加的数字比当前最小的数字大是不用管的。毕竟题目只有个PopSmallest，怎么着也管不到那个较大的数上去。