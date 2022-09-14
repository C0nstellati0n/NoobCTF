# SignIn

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=b9b2c51c-a545-4d2f-ba34-a58d8d040115_2)

废物不会系统函数。

看看main。

```c
undefined8 Main(void)
{
  int iVar1;
  long in_FS_OFFSET;
  undefined local_4a8 [16];
  undefined local_498 [16];
  undefined local_488 [16];
  undefined local_478 [16];
  undefined input [112];
  undefined local_3f8 [1000];
  long local_10;
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  puts("[sign in]");
  printf("[input your flag]: ");
  __isoc99_scanf(&format,input);
  FUN_0010096a(input,local_3f8);
  __gmpz_init_set_str(local_478,"ad939ff59f6e70bcbfad406f2494993757eee98b91bc244184a377520d06fc35",
                      16);
  __gmpz_init_set_str(local_488,local_3f8,16);
  __gmpz_init_set_str(local_4a8,
                      "103461035900816914121390101299049044413950405173712170434161686539878160984549"
                      ,10);
  __gmpz_init_set_str(local_498,"65537",10);
  __gmpz_powm(local_488,local_488,local_498,local_4a8);
  iVar1 = __gmpz_cmp(local_488,local_478);
  if (iVar1 == 0) {
    puts("TTTTTTTTTTql!");
  }
  else {
    puts("GG!");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

道理我都懂，可是那一串以__gmpz开头的都是啥？不知道为啥我直接搜这个函数没搜出来函数的介绍，直接搜出来了[wp](https://blog.csdn.net/xiao__1bai/article/details/120002976)。行吧不看白不看，我只看函数部分，真的。

- __gmpz_init_set_str 其实就是 mpz_init_set_str int mpz_init_set_str (mpz_t rop, const char \*str, int base) 函数：
<br>这三个参数分别是多精度整数变量，字符串，进制。 这个函数的作用就是将 str 字符数组以 base 指定的进制解读成数值并写入 rop 所指向的内存。<br>
<br>.
void gmpz_powm (mpz_t rop, const mpz_t base, const mpz_t exp, const mpz_t mod) 函数：
其实就是计算 base 的 exp 次方，并对 mod 取模，最后将结果写入 rop 中， 这个运算的过程和RSA的加密过程一样。<br>
<br>.
接下来就是__gmpz_cmp函数，看这个函数名就知道这是比较函数。
gmpz_cmp(b, c)； //b 大于 c，返回 1；b
等于 c，返回 0；b 小于 c，返回-1*/<br>
<br>.
重述一下就是：
gmpz_powm(op1,op2,op3,op4)； //求幂模函数 即 op1=op2^op3 mod op4;<br>
gmpz_init_set_str(b, “200000”, 10)； //即 b=200000，十进制<Br>
gmpz_cmp(b, c)； //b 大于 c，返回 1；b 等于 c，返回 0；b 小于 c，返回-1*/

我最开始有注意到powm可能是powmod的缩写，但是猜不到为什么会有4个参数。原来参数1是存储结果的，c语言里很多函数都这样。c语言我恨你。

powmod加65537，这不是rsa吗？如果按照rsa的想法，local_488是我们的输入的密文，local_478是正确的密文，local_498是e也就是65537，local_4a8是n。n很小，可以直接factordb得到p和q，后面就是正常rsa了。

```python
from Crypto.Util.number import inverse,long_to_bytes
c=int("ad939ff59f6e70bcbfad406f2494993757eee98b91bc244184a377520d06fc35",16)
p=282164587459512124844245113950593348271
q=366669102002966856876605669837014229419
phi=(p-1)*(q-1)
d=inverse(65537,phi)
print(long_to_bytes(pow(c,d,p*q)))
```

这个操作都快被我刻在dna里了。

- ### Flag
  > suctf{Pwn_@_hundred_years}