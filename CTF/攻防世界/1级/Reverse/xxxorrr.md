# xxxorrr

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=12cac856-1c80-11ed-9802-fa163e4fa66d)

小看1级题然后被坑了。

ghidra反编译出来怪怪的，检查输入的函数在接收和加密输入的前面。不是什么大问题，知道那个意思就得了。

```c
undefined8 Main(void)
{
  long in_FS_OFFSET;
  int local_3c;
  byte local_38 [40];
  long local_10;
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  FUN_00100a90(CheckFlag);
  fgets((char *)local_38,35,stdin);
  for (local_3c = 0; local_3c < 34; local_3c = local_3c + 1) {
    s_qasxcytgsasxcvrefghnrfghnjedfgbh_00301020[local_3c] =
         local_38[local_3c] ^ s_qasxcytgsasxcvrefghnrfghnjedfgbh_00301020[local_3c];
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

关键数据的每一位与输入疑惑，接着检查结果是否与下面函数中出现的值相同。

```c
void CheckFlag(void)
{
  long lVar1;
  int iVar2;
  long in_FS_OFFSET;
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  iVar2 = strcmp(s_qasxcytgsasxcvrefghnrfghnjedfgbh_00301020,&DAT_00301060);
  if (iVar2 == 0) {
    puts("Congratulations!");
  }
  else {
    puts("Wrong!");
  }
  if (lVar1 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

期望值为DAT_00301060。异或谁都会，但是你会发现这样出来是乱码。怎么回事呢？有两种方法：第一种是找关键字符串s_qasxcytgsasxcvrefghnrfghnjedfgbh_00301020在程序中的全部引用，第二种是手动翻程序中所有的函数。一个初始化用的函数竟然对关键数据做了改变。

```c
void _INIT_1(void)
{
  long lVar1;
  long in_FS_OFFSET;
  int i;
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  for (i = 0; i < 34; i = i + 1) {
    s_qasxcytgsasxcvrefghnrfghnjedfgbh_00301020[i] =
         s_qasxcytgsasxcvrefghnrfghnjedfgbh_00301020[i] ^ (char)i * 2 + 65U;
  }
  if (lVar1 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

把这段加上就能得到真正的flag了。不知道为啥我逆向出来少了个}符号，不过不影响。

```python
expected_value='56 4e 57 58 51 51 09 46 17 46 54 5a 59 59 1f 48 32 5b 6b 7c 75 6e 7e 6e 2f 77 4f 7a 71 43 2b 26 89 fe'.split(' ')
s='71 61 73 78 63 79 74 67 73 61 73 78 63 76 72 65 66 67 68 6e 72 66 67 68 6e 6a 65 64 66 67 62 68 6e'.split(' ')
for i in range(len(s)):
   s[i]=int(s[i],16)^i*2+65
for i in range(len(s)):
   print(chr(s[i]^int(expected_value[i],16)),end='')
```

知识点：

1.初始化用的函数里也能藏操作<br>
2.对程序中的数据有问题时记得查找其引用，看看有没有被偷偷更改过<br>

- ### Flag
  > flag{c0n5truct0r5_functi0n_in_41f}