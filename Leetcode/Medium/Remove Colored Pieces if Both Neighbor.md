# Remove Colored Pieces if Both Neighbors are the Same Color

[题目](https://leetcode.com/problems/remove-colored-pieces-if-both-neighbors-are-the-same-color)

看了hint就会做了。但我这辈子注定与优雅代码无缘。
```c#
public class Solution {
    public bool WinnerOfGame(string colors) {
        if(colors.Length<=2){
            return false;
        }
        int alice=0;
        int bob=0;
        int aCount=0;
        int bCount=0;
        foreach(char c in colors){
            if(c=='A'){
                aCount++;
                if(bCount>=3){
                    bob+=bCount-2;
                }
                bCount=0;
            }
            else if(c=='B'){
                bCount++;
                if(aCount>=3){
                    alice+=aCount-2;
                }
                aCount=0;
            }
        }
        if(bCount>=3){
            bob+=bCount-2;
        }
        if(aCount>=3){
            alice+=aCount-2;
        }
        return alice>bob;
    }
}
```
```
Runtime
58 ms
Beats
100%
Memory
42.6 MB
Beats
57.69%
```
这么长一串鬼东西完全等同于下面的：
```c#
//采样区
//leetcode的数据真的只能做参考，有运气的成分
public class Solution {
    public bool WinnerOfGame(string colors) {
        int length = colors.Length;
        int countAliceMove = 0;
        int countBobMove = 0;
        for (int i = 1; i < length - 1; i++){
            if (colors[i - 1] != colors[i] || colors[i] != colors[i + 1]){ //3个同样颜色的color才起步开始算
                continue;
            }
            if (colors[i] == 'A'){
                countAliceMove++;
            }
            else{
                countBobMove++;
            }
        }
        return countAliceMove > countBobMove;
    }
}
```
```
Runtime
59 ms
Beats
100%
Memory
42.7 MB
Beats
57.69%
```