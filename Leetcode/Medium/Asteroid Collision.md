# Asteroid Collision

[题目](https://leetcode.com/problems/asteroid-collision/description/)

总是看了解法后才知道hint说的原来是这个意思。
```c#
//https://leetcode.com/problems/asteroid-collision/editorial/ ,但是采样区最佳。思路一致但是实现方式不一样
public class Solution {
    public int[] AsteroidCollision(int[] asteroids) { 
        Stack<int> stack = new(); //stack代表当前asteroid的稳定形式

        for (int i = 0; i < asteroids.Length; ++i)
        {
            while(stack.Count != 0 && asteroids[i] < 0 && stack.Peek() > 0) //关于为什么是asteroids[i] < 0 && stack.Peek() > 0，因为这道题默认正数往右走（数组末尾），负数往左走（数组开头）
            //所以无需检查asteroids[i] > 0 && stack.Peek() < 0的情况，stack里的小行星一定是比当前asteroids[i]在更左边的，这种情况无论如何都撞不到
            {
                int temp = asteroids[i] + stack.Peek(); //撞一下看结果
                if (temp > 0) //asteroids[i]比stack.Peek()更小，销毁asteroids[i]
                {
                    asteroids[i] = 0;
                } 
                else if (temp < 0) //反之则是把stack最顶上的pop掉
                {
                    stack.Pop();
                }
                else //两者一样大，都没了
                {
                    asteroids[i] = 0;
                    stack.Pop();
                }
            }
            
            if (asteroids[i] != 0) //上面的while循环有个stack.Count != 0 ，所以第一次肯定能进来这里。又根据constraint，单个asteroid不会为0。所以我们在上面把撞毁的asteroid设为0
            {
                stack.Push(asteroids[i]); //第一次循环，一个asteroid，就一个的话肯定是稳定状态
            }
        }

        int[] result = new int[stack.Count];
        result = stack.ToArray();
        Array.Reverse(result);
        return result;
    }
}
```
```
Runtime
139 ms
Beats
95.93%
Memory
46.4 MB
Beats
22.4%
```
我自己做的时候就是忽略了“正数往右走（数组末尾），负数往左走（数组开头）”这个条件，结果想得太复杂了，直接放弃了。