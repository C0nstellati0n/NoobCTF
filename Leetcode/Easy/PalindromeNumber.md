# Palindrome Number

[题目地址](https://leetcode.com/problems/palindrome-number/)

Given an integer x, return true if x is a palindrome,and false otherwise。判断给定数字x是否是回文数字。

我自己的思路是将数字转为字符串，然后反转，比对反转结果和原字符串是否相同。就像下面这样：

```c#
public class Solution {
    public bool IsPalindrome(int x) {
        string str=x.ToString();
        char[] arr = str.ToCharArray();
        Array.Reverse(arr);
        return new string(arr)==str;
    }
}
```

提交后去看了官方解。我这个方法确实是大部分人的第一想法，但是有个问题：

- 转的过程中需要另外的内存

另一种办法则是直接在数字身上考虑了。我开始也这么想过，但是没有字符串好操作就放弃了。官方解如下：

```c#
public class Solution {
    public bool IsPalindrome(int x) {
        // Special cases:
        // As discussed above, when x < 0, x is not a palindrome.
        // Also if the last digit of the number is 0, in order to be a palindrome,
        // the first digit of the number also needs to be 0.
        // Only 0 satisfy this property.
        if(x < 0 || (x % 10 == 0 && x != 0)) {
            return false;
        }

        int revertedNumber = 0;
        while(x > revertedNumber) {
            revertedNumber = revertedNumber * 10 + x % 10;
            x /= 10;
        }

        // When the length is an odd number, we can get rid of the middle digit by revertedNumber/10
        // For example when the input is 12321, at the end of the while loop we get x = 12, revertedNumber = 123,
        // since the middle digit doesn't matter in palidrome(it will always equal to itself), we can simply get rid of it.
        return x == revertedNumber || x == revertedNumber/10;
    }
}
```

这两种解法又是时间和空间的交换。第一个解运行时间超越77%的人，但是内存仅超越30%的人；数字版本则是反过来，运行时间仅超越46%的人，而内存超越75%的人。就看平时的选择了。