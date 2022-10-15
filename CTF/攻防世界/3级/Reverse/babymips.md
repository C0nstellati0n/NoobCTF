# babymips

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=dc2f75d9-a755-4991-aaa9-bf5a99868510_2)

位运算真的太奇妙了。

虽然是mips，但是该怎么逆就怎么逆，没啥变化。

```c
void Main(void)

{
  int iVar1;
  int i;
  byte input [36];
  
  setbuf(stdout,(char *)0x0);
  setbuf(stdin,(char *)0x0);
  printf("Give me your flag:");
  scanf("%32s",input);
  for (i = 0; i < 0x20; i = i + 1) {
    input[i] = input[i] ^ 0x20U - (char)i;
  }
  iVar1 = strncmp((char *)input,_fdata,5);
  if (iVar1 == 0) {
    SecondEncode(input);
  }
  else {
    puts("Wrong");
  }
  return;
}
```

flag长0x20，首先把整个输入异或0x20，然后前5位与_fdata相比。如果一致，进行后续的比对。

```c
void SecondEncode(char *param_1)

{
  size_t sVar1;
  int iVar2;
  uint i;
  
  for (i = 5; sVar1 = strlen(param_1), i < sVar1; i = i + 1) {
    if ((i & 1) == 0) {
      param_1[i] = (byte)((uint)((int)param_1[i] << 0x1a) >> 0x18) | param_1[i] >> 6;
    }
    else {
      param_1[i] = param_1[i] >> 2 | (byte)((uint)((int)param_1[i] << 0x1e) >> 0x18);
    }
  }
  iVar2 = strncmp(param_1 + 5,PTR_DAT_00410d04,27);
  if (iVar2 == 0) {
    puts("Right!");
  }
  else {
    puts("Wrong!");
  }
  return;
}
```

一些位操作，要求操作后结果等同于PTR_DAT_00410d04这个指针里的内容（注意是指针）。逻辑非常清晰，就是不知道后部分该怎么逆向。我第一次想到的是爆破，也可以，但不是这道题的精髓。

```c
param_1[i] = (byte)((uint)((int)param_1[i] << 0x1a) >> 0x18) | param_1[i] >> 6;
param_1[i] = param_1[i] >> 2 | (byte)((uint)((int)param_1[i] << 0x1e) >> 0x18);
```

仔细看这两行，似乎很复杂，还涉及了按位或，按照之前的经验是无法逆向的。其实这行代码所做的操作完全有迹可循，比如第一行是把低6位和高2位为进行交换，第二行是把低2位和高6为进行交换。还可以这么表示,会更清晰：

```c
param_1[i] = (byte)((uint)((int)param_1[i] << 2)) | param_1[i] >> 6;
param_1[i] = param_1[i] >> 2 | (byte)((uint)((int)param_1[i] << 6));
```

拿第二行举例，如果一个数是00000011，交换后就得到11000000。不难发现两个操作之间互为逆运算，我们只需要把最开始判断奇偶数的判断if ((i & 1) == 0)取反后直接抄就能逆向flag了。

```python
flag="Q|j{g"
flag=list(map(ord,flag))
flag+=[0x52,0xFD,0x16,0xA4,0x89,0xBD,0x92,0x80,0x13,0x41,0x54,0xA0,0x8D,0x45,0x18,0x81,0xDE,0xFC,0x95,0xF0,0x16,0x79,0x1A,0x15,0x5B,0x75,0x1F]
for i in range(5,32):
    if i&1!=0:
        flag[i]=(((flag[i]<<0x1a))>>0x18|(flag[i]>>6))&0xFF
    else:
        flag[i]=((flag[i]>>2)|((flag[i]<<0x1e))>>0x18)&0xFF
for i in range(32):
    flag[i]=chr(flag[i]^(32-i))
print(''.join(flag))
```

可以像这么写，用上面提到的清晰方法写也行。&0xff是为了丢掉超过8位的高位，因为c语言里int只有8位，超过自动丢弃，但python里可没有这种说法，所以要手动丢弃。

- ### Flag
  > qctf{ReA11y_4_B@89_mlp5_4_XmAn_}