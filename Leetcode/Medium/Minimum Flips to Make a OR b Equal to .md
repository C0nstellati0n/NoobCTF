# Minimum Flips to Make a OR b Equal to c

[题目](https://leetcode.com/problems/minimum-flips-to-make-a-or-b-equal-to-c/description/)

在discussion看到了用[BitArray](https://learn.microsoft.com/en-us/dotnet/api/system.collections.bitarray?view=net-7.0)的提示，于是我用了。简单是简单，就是bitarray似乎有点多余。
```c#
public class Solution {
    public int MinFlips(int a, int b, int c) {
        if((a|b)==c){
            return 0;
        }
        int count=0;
        BitArray ar = new BitArray(new int[] { a });
        BitArray br = new BitArray(new int[] { b });
        BitArray cr = new BitArray(new int[] { c });
        for(int i=0;i<ar.Count;i++){
            if((ar[i]|br[i])!=cr[i]){
                switch(cr[i]){
                    case true: //bitarray里的元素是true和false，不是1和0
                        count++;
                        break;
                    case false:
                        if(ar[i]==true&&br[i]==true){
                            count+=2;
                        }
                        else{
                            count++;
                        }
                        break;
                }
            }
        }
        return count;
    }
}
```
```
Runtime
21 ms
Beats
80.56%
Memory
27.1 MB
Beats
13.89%
```
为啥说bitarray多余呢？因为可以直接用位运算取bit。
```c#
//https://leetcode.com/problems/minimum-flips-to-make-a-or-b-equal-to-c/solutions/3606668/python-java-c-simple-solution-easy-to-understand/
class Solution {
    public int MinFlips(int a, int b, int c) {
        int flips = 0;
        while (a > 0 || b > 0 || c > 0) {
            int bitA = a & 1;
            int bitB = b & 1;
            int bitC = c & 1;

            if (bitC == 0) {
                flips += (bitA + bitB); 
            } else {
                if (bitA == 0 && bitB == 0) {
                    flips += 1; 
                }
            }

            a >>= 1;
            b >>= 1;
            c >>= 1;
        }
        return flips;
    }
}
```
```
Runtime
21 ms
Beats
80.56%
Memory
26.9 MB
Beats
25%
```
或者不改动a，b和c本身，用mask取bit。
```c#
//https://leetcode.com/problems/minimum-flips-to-make-a-or-b-equal-to-c/solutions/477690/java-python-3-bit-manipulation-w-explanation-and-analysis/
public class Solution {
    public int MinFlips(int a, int b, int c) {
        int ans = 0, ab = a | b, equal = ab ^ c;
        for (int i = 0; i < 31; ++i) {
            int mask = 1 << i;
            if ((equal & mask) > 0)  // ith bits of a | b and c are not same, need at least 1 flip.
             // ans += (ab & mask) < (c & mask) || (a & mask) != (b & mask) ? 1 : 2;
                ans += (a & mask) == (b & mask) && (c & mask) == 0 ? 2 : 1; // ith bits of a and b are both 1 and that of c is 0?
        }
        return ans;
    }
}
```
```
Runtime
23 ms
Beats
75%
Memory
26.8 MB
Beats
58.33%
```
再或者用PopCount函数（用于计算数字二进制中1的数量，参考 https://stackoverflow.com/questions/109023/count-the-number-of-set-bits-in-a-32-bit-integer ）,一行搞定。
```c#
//https://leetcode.com/problems/minimum-flips-to-make-a-or-b-equal-to-c/solutions/479998/c-bitwise-xor-solution-1-line/
public class Solution {
    public int MinFlips(int a, int b, int c) {
        return System.Numerics.BitOperations.PopCount((uint)((a | b) ^ c)) + System.Numerics.BitOperations.PopCount((uint)(a & b & ((a | b) ^ c)));
    }
}
```
```
Runtime
20 ms
Beats
83.33%
Memory
26.9 MB
Beats
25%
```