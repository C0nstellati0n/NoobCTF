# broken-box

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=b757ac5c-462a-4448-8fac-2452ea1a3e55_2&task_category_id=5)

又少附件了。(⌒-⌒; )完整题目+wp参考[这里](https://github.com/ernw/ctf-writeups/tree/master/csaw2016/broken_box)。

按照完整的题目附件，我们有flag.enc，也就是flag的rsa密文形式。同时给了一个nc地址，将0-9999的数字签名后并返回。e为65537。连接nc，输入两次同样的数字，结果不一样，照应了题目描述的“硬件坏了”。先要知道rsa中的签名是什么。

- pow(data, d, n) = sig

假如签名正确的话，我们可以用e来恢复data。

- pow(sig,e,n) = data

现在data可控，e与n已知，签名有点坏了。现在就是猜测签名的步骤哪一步可能有问题。n没有问题，因为手动测试时发现给出的n每次都是一样的。data不能有问题，那只能是d有问题了。再根据题目描述“有些bit被翻转了”，猜测d中有些二进制位从0变成了1或者反过来。验证第一次输入2时的签名2261……，得到2，说明这个签名是没问题的，那么之后继续输入2后得到的签名一旦不一样就都是错的。猜测d每次翻转1位（不知道大佬们怎么猜出来的，可能别的不太可能了，翻转一位的情况最简单，所以先猜这个），掏出代数武器。

如果d的第k个bit从1变为0，那么$d'=d-2^k$。因此有$data^{d'} = data^{d - 2^k} = \frac{data^d}{data^{2^k}} \mod k$。

反过来，如果d的第k个bit从0变为1，那么$d'=d+2^k$。因此有$data^{d'}=data^{d+2^k}=data^d*data^{2^k}\mod k$。

如果接受到的无效签名=之前得到的有效签名*pow(2, pow(2, k, n), n),说明第k个bit之前是0，现在变成1了。k，也就是第几位变了，虽然不知道，但是可以爆破啊，只有1024种可能。反过来决定从1变成0的同理。

没有脚本，以上内容来自此[wp](https://github.com/p4-team/ctf/tree/master/2016-09-16-csaw/broken_box)。看的wp里最清晰的。

- ### Flag
  > flag{br0k3n_h4rdw4r3_l34d5_70_b17_fl1pp1n6}