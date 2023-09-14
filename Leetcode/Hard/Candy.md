# Candy

[题目](https://leetcode.com/problems/candy)

照着discussion区的提示莫名其妙就写出来了。
```c#
public class Solution {
    public int Candy(int[] ratings) {
        int[] arr=new int[ratings.Length];
        for(int i=1;i<ratings.Length;i++){
            if(ratings[i]>ratings[i-1]){ //先正着遍历，根据题目要求，若i处的rating比i-1处的rating高，就增加1
                arr[i]=arr[i-1]+1;
            }
        }
        for(int i=ratings.Length-2;i>=0;i--){ //然后倒着遍历
            if(ratings[i]>ratings[i+1]){
                if(arr[i]<=arr[i+1]){ //注意若i处rating大于i-1处rating，i处candy的数量至少要是i-1处的candy数量+1。注意到给i处增加candy数量不会影响之前正着遍历时i和i-1之间的candy关系
                    arr[i]=arr[i+1]+1;
                }
            }
        }
        return arr.Sum()+ratings.Length;
    }
}
```
```
Runtime
84 ms
Beats
96.76%
Memory
44.5 MB
Beats
37.58%
```
我不满意，space不行。能不能O(1)?
```c#
//https://leetcode.com/problems/candy/solutions/4037652/beats-99-93-greedy-two-solutions-c-java-python-commented-code
public class Solution {
    public int Candy(int[] ratings) {
        int ret=1;
        int up=0; //递增序列的连续数量
        int down=0; //递减序列的连续数量
        int peak=0; //上一个递增序列的candy最高值
        int prev;
        int curr;
        for(int i=0;i<ratings.Length-1;i++){
            prev=ratings[i];
            curr=ratings[i+1];
            if(prev<curr){ //严格递增
                up=peak=up+1;
                down=0;
                ret+=1+up; //1是基础的candy，每个人都至少有一个candy。严格递增的话就一个一个加
            }
            else if(prev==curr){ //根据题目描述，若不是递增的话，对应给的candy数量可以是最小的1
                up=down=peak=0;
                ret+=1;
            }
            else{ //虽然这块是递减的，但我总感觉计算ret的逻辑还是按照递增的来的。假如从递增序列换到递减序列的话，目前down是1，peak大于down。所以递减序列的第一个元素对应ret+=1
            //递减序列的第二个元素对应ret+=2。实际上递减序列的第二个元素应该对应比第一个元素更多的candy，所以我感觉它是从递减序列的最后一个元素开始算的
                up=0;
                down++;
                ret+=1+down-(peak>=down?1:0); //(peak>=down?1:0)我感觉是为了处理上一个递增序列最高不如递减序列的情况。比如上一个递增序列长度为3，但递减序列长度为4。这时down就不会减去那个1，而这个没减去的1是给上一个递增序列的peak留的
            }
        }
        return ret;
    }
}
```
```
Runtime
82 ms
Beats
98.70%
Memory
43.9 MB
Beats
89.63%
```