# [Flatten Nested List Iterator](https://leetcode.com/problems/flatten-nested-list-iterator)

C#是被抛弃的那个，java，c++都用自带的iterator，只有c#我搜了半天不知道怎么拿。
```c#
//https://leetcode.com/problems/flatten-nested-list-iterator/solutions/4187840/95-83-recursive-flattening-stack
public class NestedIterator {
    private List<int> flattened;
    private int index;
    public NestedIterator(IList<NestedInteger> nestedList) {
        flattened = new List<int>();
        index = 0;
        flattened = Flatten(nestedList); //这个解法的要点在于直接在构造函数就把数字全部扁平化，记在flattened里。后面要用直接拿
    }
    private List<int> Flatten(IList<NestedInteger> nested) { //递归拿数字
        List<int> result = new List<int>();
        foreach (var ni in nested) {
            if (ni.IsInteger()) { //是数字就直接加
                result.Add(ni.GetInteger());
            } else {
                result.AddRange(Flatten(ni.GetList())); //不是数字就取出里面的list，递归进行flatten
            }
        }
        return result;
    }
    public int Next() {
        return flattened[index++];
    }
    public bool HasNext() {
        return index < flattened.Count;
    }
}
```
递归就属于那种很好理解但是可能不是很好想的做法。采样区还有个不递归的做法
```c#
public class NestedIterator {
    Stack<NestedInteger> stack;
    public NestedIterator(IList<NestedInteger> nestedList)
    {
        stack = new();
        int l = nestedList.Count;
        for (int i = l - 1; i >= 0; i--)
        {
            stack.Push(nestedList[i]); //倒序将nestedList push进stack，这样pop时就是从第一个开始
        }
    }
    public bool HasNext() {
        UnWrapLast();
        return stack.Count > 0;
    }
    public int Next() {
        UnWrapLast();
        return stack.Pop().GetInteger(); //UnWrapLast保证了栈顶一定是数字
    }
    private void UnWrapLast()
    {
        while (stack.Count > 0 && !stack.Peek().IsInteger()) //保证栈顶一定是数字，如果不是就扁平化栈顶这个list
        {
            var list = stack.Pop().GetList();
            int l = list.Count;
            for (int i = l - 1; i >= 0; i--)
            {
                stack.Push(list[i]); //倒着push进去，和上面一样的道理。因为是while语句，若栈顶还不是数字，继续扁平化
            }
        }
    }
}
```
我耿耿于怀改不出来的做法： https://leetcode.com/problems/flatten-nested-list-iterator/solutions/80146/real-iterator-in-python-java-c