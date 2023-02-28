# Plus One

[题目](https://leetcode.com/problems/plus-one/)

给定一个数组表示的数字，从左至右为高位到低位，返回加一后的数字的数组表达形式。最开始想把数组转为字符串再转为数字然后加上一再转回数组，结果发现后面数字太大了，转数字会溢出。于是写了下面这个垃圾代码。

```c#
public class Solution {
    public int[] PlusOne(int[] digits) {
        List<int> output=new();
        int temp=(digits[^1]+1)/10;
        output.Add((digits[^1]+1)%10);
        for(int i=digits.Length-2;i>=0;i--){
            output.Add((digits[i]+temp)%10);
            temp=(digits[i]+temp)/10;
        }
        //最开始是while，后面觉得+1最多增加一位，就只写了个if
        if(temp!=0){
            output.Add(temp%10);
        }
        output.Reverse();
        return output.ToArray();
    }
}
```

```
Runtime
140 ms
Beats
64.41%
Memory
42.5 MB
Beats
17.17%
```

明明我都注意到只加1这个关键点了，怎么写的还那么复杂呢？去看了下大佬的解，思路清晰且简单。

```c#
public class Solution {
    public int[] PlusOne(int[] digits) {
        for (int i = digits.Length - 1; i >= 0; i--) {
	        if (digits[i] < 9) {
		        digits[i]++;
		        return digits;
		// starting from extreme right--> if array[i] is less than 9 means can be added with 1
		// i.e. [ 5,8 ]-->[ 5,9 ] or
		//      [ 9,4 ]-->[ 9,5 ] or
		//      [ 6,0 ]-->[ 6,1 ]
		// and will directly return array
	        }
            digits[i] = 0;
        // if array[i] is not less than 9, means it have to be 9 only then digit is changed to 0,
	// and we again revolve around loop to check for number if less than 9 or not
	// i.e. [ 5,9 ]-->[ 5,0 ]-loop->[ 6,0 ] or
	//      [ 1,9,9 ]-->[ 1,9,0 ]-loop->[ 1,0,0 ]-loop->[ 2,0,0 ]
	// and will directly return array
        }
        // if all number inside array are 9
// i.e. [ 9,9,9,9 ] than according to above loop it will become [ 0,0,0,0 ]
// but we have to make it like this [ 9,9,9,9 ]-->[ 1,0,0,0,0 ]


// to make like above we need to make new array of length--> n+1
// by default new array values are set to -->0 only
// thus just changed first value of array to 1 and return the array

        digits = new int[digits.Length + 1];
        digits[0] = 1;
        return digits;
    }
}
```

```
Runtime
140 ms
Beats
64.41%
Memory
42 MB
Beats
68.69%
```

不用过多解释，大佬已经写了简洁明了的注释了。接下来又是另一种做法。

```c#
public class Solution {
    public int[] PlusOne(int[] digits) {
        List<int> res=new(digits);
        int n = digits.Length;
        for(int i = n-1; i >= 0; i--){
            if(i == n-1) //从右数最后一位加一
                res[i]++;
            if(res[i] == 10){ //9+1=10的情况
                res[i] = 0; //当前位改为0
                if(i != 0){ //不是首位的情况
                    res[i-1]++; //进位，左边的数字进位1
                }
                else{
                    res.Add(0); //是首位说明要增加一位0，第一位是1
                    res[i] = 1;
                }
            }
        }
        return res.ToArray();
    }
}
```

该算法的表现有点神奇，第一次提交表现非常一般，甚至比我写的那个还差。我不信邪，又提交了一次，获得有史以来最好成绩。

```
Runtime
122 ms
Beats
99.1%
Memory
42.2 MB
Beats
58.46%
```

改编自下面的c++实现。c++里面的vector类似于可变数组，在我看来和c#里面的list有点像。那很坑的地方来了，为什么C#参数是数组而不是列表啊？如果我想仿写算法，只能转列表后面再转数组……都什么年代了还在用传统数组啊（doge）？

```c++
class Solution {
public:
    vector<int> plusOne(vector<int>& v) {
        int n = v.size();
        for(int i = n-1; i >= 0; i--){
            if(i == n-1)
                v[i]++;
            if(v[i] == 10){
                v[i] = 0;
                if(i != 0){
                    v[i-1]++;
                }
                else{
                    v.push_back(0);
                    v[i] = 1;
                }
            }
        }
        return v;
    }
};
```