# Add Binary

[题目](https://leetcode.com/problems/add-binary/)

给出两个数组表示的二进制字符串，返回两者相加的二进制结果的数组形式。硬要写也不是很难，然而我看着自己那乱七八糟的代码——关键还不过，决定直接看答案节省时间。依旧是不能直接转数字相加再转二进制，会溢出。

```c#
public class Solution {
    public string AddBinary(string a, string b) {
        StringBuilder res = new StringBuilder();
        int i = a.Length - 1;
        int j = b.Length - 1;
        int carry = 0;
        while(i >= 0 || j >= 0){
            int sum = carry;
            if(i >= 0){
                sum += a[i] - '0';
                i--;
            }
            if(j >= 0){ 
                sum += b[j] - '0'; //字符值减去'0'就能获得其对应的数字值。例如'9'-'0'=9
                j--;
            }
            carry = sum > 1 ? 1 : 0;
            res.Append(sum % 2);
        }
        if(carry != 0){ 
            res.Append(carry);
        }
        return new string(res.ToString().Reverse().ToArray()); //原版java代码为return res.reverse().toString(); ，c#不知道怎么搞，就堆了个这玩意
    }
}
```

```
Runtime
74 ms
Beats
92.1%
Memory
39.1 MB
Beats
42.91%
```

比较直白的做法如下：

```c#
public class Solution {
    public string AddBinary(string a, string b) {
        if(b.Length > a.Length) (a, b) = (b, a); //https://stackoverflow.com/questions/552731/c-good-best-implementation-of-swap-method 学到的字符串交换方法
        while(b.Length < a.Length) b = "0" + b;
        int carry = 0;
        string res = "";
        for(int i = b.Length-1; i >= 0 ; --i)
        {
             
             if(b[i] == '1' && a[i]=='1')
             {

                if(carry == 0) res = "0" + res;
                
                else res = "1" + res;
                    
                carry = 1;
             }

             else if(b[i] =='0' && a[i] =='0')
             {

                if(carry == 0) res = "0" + res;
                 
                else
                {
                    res = "1" + res;
                    carry = 0;
                }
             }

             else if((b[i]=='0' && a[i]=='1') || (b[i]=='1' && a[i] == '0'))
             {
                 
                if(carry == 0) res = "1" + res;
                 
                else res = "0" + res;
                 
             }
             
        }
        if(carry == 1) res = "1" + res;
        
        return res;
    }
}
```

```
Runtime
77 ms
Beats
85.51%
Memory
42.1 MB
Beats
5.27%
```

用时还行，内存直接裂开。