# Repeated Substring Pattern

[题目](https://leetcode.com/problems/repeated-substring-pattern/description/)

看到是easy的我：这么简单，肯定不费吹灰之力就拿下！

发现discussion提到的三种思路自己两种不懂的我：啊？？？

建议直接看[editorial](https://leetcode.com/problems/repeated-substring-pattern/editorial/)，我到最后连爆破都没写出来。因为discussion里有人说“当字符串长度为质数时，检查字符串是否完全由一个字符组成，否则返回false”，我就卡在了怎么检查质数。（去搜了但是懒得写，暴力有啥意思呢？对……对吧？）。editorial介绍了爆破和神奇的字符串拼接做法（就是discussion里vyshnavkr提到的String rotation OR Concatenation做法，代码不难但是很巧妙）

但是我想在这里说的是，我去看了采样区，这tm是什么东西？
```c#
public class Solution {
  public bool RepeatedSubstringPattern(string s) {
    var str = s.AsSpan();
    Span<char> ss = stackalloc char[s.Length * 2];
    str.CopyTo(ss.Slice(0,str.Length));
    str.CopyTo(ss.Slice(str.Length, str.Length));
    return MemoryExtensions.Contains(ss[1..^1], str,StringComparison.Ordinal);
  }
}
```
```
Runtime
71 ms
Beats
86.28%
Memory
46 MB
Beats
88.5%
```
看了这个解法我才知道，我懂个鬼的c#。后来去查了下[AsSpan](https://learn.microsoft.com/en-us/dotnet/api/system.memoryextensions.asspan?view=net-7.0)，大概就是说“Creates a new read-only span over a string.”。哦，就是把字符串转成个只读span。关键AsSpan才是官方推荐的，什么Substring，Range-based indexers，都不如这个我如此面生的家伙。
- [Prefer AsSpan over Substring](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca1846)
- [Use AsSpan instead of Range-based indexers for string when appropriate](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca1831)

好，[stackalloc](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/operators/stackalloc)又是什么？啥？“在栈上分配内存，当方法返回时自动丢弃。不能手动回收stackalloc分配的内存，GC不管它……”。你别说还挺不错，这个功能早在2009年就有了我现在才知道……
- [Practical use of `stackalloc` keyword](https://stackoverflow.com/questions/785226/practical-use-of-stackalloc-keyword)
- [Dos and Don'ts of stackalloc](https://vcsjones.dev/stackalloc/)

stackalloc返回的是Span。[CopyTo](https://learn.microsoft.com/en-us/dotnet/api/system.readonlyspan-1.copyto?view=net-7.0)就挺好理解的，把str readonlyspan里的内容拷贝到ss span中。[slice](https://learn.microsoft.com/en-us/dotnet/api/system.span-1.slice?view=net-7.0)就是单纯的切割。[MemoryExtensions.Contains](https://learn.microsoft.com/en-us/dotnet/api/system.memoryextensions.contains?view=net-7.0)返回内容是否出现在span中。StringComparison.Ordinal表示“Compare strings using ordinal (binary) sort rules“（https://learn.microsoft.com/en-us/dotnet/api/system.stringcomparison?view=net-7.0）。其实就是String rotation OR Concatenation，但是用了官方推荐的span然后就变得不熟悉了。

以及[KMP算法](https://www.zhihu.com/question/21923021)解法： https://leetcode.com/problems/repeated-substring-pattern/solutions/94397/c-o-n-using-kmp-32ms-8-lines-of-code-with-brief-explanation/ 。但是我不太懂，这题用的也是变种。懒得看了，下次遇见纯正KMP再记。