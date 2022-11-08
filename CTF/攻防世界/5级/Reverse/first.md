# first

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=29aafc91-11ea-4828-998d-d40aef34070c_2)

好难，我好菜。

```c
undefined8 Main(void)

{
  char cVar1;
  pthread_t __th;
  int iVar2;
  uint uVar3;
  uint uVar4;
  time_t tVar5;
  long lVar6;
  char *pcVar7;
  uint *puVar8;
  uint *puVar9;
  ulong uVar10;
  ulong isCorrect;
  byte bVar11;
  int *piVar12;
  int *piVar13;
  pthread_t *ppVar14;
  void *__arg;
  pthread_t *__newthread;
  bool bVar15;
  
  tVar5 = time((time_t *)0x0);
  srand((uint)tVar5);
  piVar12 = &DAT_006021f0;
  do {
    iVar2 = rand();
    piVar13 = piVar12 + 1;
    *piVar12 = (iVar2 % 1000) * 100;
    piVar12 = piVar13;
  } while (piVar13 != (int *)&DAT_00602208);
  __isoc99_scanf();
  puVar9 = &DAT_00602180;
  do {
    puVar8 = puVar9;
    uVar3 = *puVar8 + 0xfefefeff & ~*puVar8;
    uVar4 = uVar3 & 0x80808080;
    puVar9 = puVar8 + 1;
  } while (uVar4 == 0);
  bVar15 = (uVar3 & 0x8080) == 0;
  if (bVar15) {
    uVar4 = uVar4 >> 0x10;
  }
  if (bVar15) {
    puVar9 = (uint *)((long)puVar8 + 6);
  }
  bVar11 = 0;
  for (lVar6 = 0; (long)puVar9 + (-0x602183 - (ulong)CARRY1((byte)uVar4,(byte)uVar4)) != lVar6;
      lVar6 = lVar6 + 1) {
    bVar11 = bVar11 ^ (char)lVar6 + *(char *)((long)&DAT_00602180 + lVar6);
  }
  ppVar14 = &DAT_00602260;
  __arg = (void *)0x0;
  __newthread = &DAT_00602260;
  do {
    iVar2 = pthread_create(__newthread,(pthread_attr_t *)0x0,start_routine,__arg);
    if (iVar2 != 0) {
      perror("pthread_create");
                    /* WARNING: Subroutine does not return */
      exit(-1);
    }
    __arg = (void *)((long)__arg + 1);
    __newthread = __newthread + 1;
  } while (__arg != (void *)0x6);
  do {
    __th = *ppVar14;
    ppVar14 = ppVar14 + 1;
    pthread_join(__th,(void **)0x0);
  } while (ppVar14 != (pthread_t *)0x602290);
  uVar10 = 0;
  while( true ) {
    puVar9 = &DAT_00602180;
    do {
      puVar8 = puVar9;
      uVar3 = *puVar8 + 0xfefefeff & ~*puVar8;
      uVar4 = uVar3 & 0x80808080;
      puVar9 = puVar8 + 1;
    } while (uVar4 == 0);
    bVar15 = (uVar3 & 0x8080) == 0;
    if (bVar15) {
      uVar4 = uVar4 >> 0x10;
    }
    if (bVar15) {
      puVar9 = (uint *)((long)puVar8 + 6);
    }
    isCorrect = (long)puVar9 + (-0x602183 - (ulong)CARRY1((byte)uVar4,(byte)uVar4));
    if (isCorrect <= uVar10) break;
    (&flag)[uVar10] = (&flag)[uVar10] ^ (&DAT_006020e0)[uVar10] ^ bVar11;
    uVar10 = uVar10 + 1;
  }
  if (isCorrect == 0) {
LAB_00400bd4:
    __printf_chk(1,"Here is the flag:%s ",&flag);
  }
  else {
    if ((byte)(flag - 0x30U) < 0x4b) {
      pcVar7 = &DAT_00602221;
      do {
        if (pcVar7 == &flag + isCorrect) goto LAB_00400bd4;
        cVar1 = *pcVar7;
        pcVar7 = pcVar7 + 1;
      } while ((byte)(cVar1 - 0x30U) < 0x4b);
    }
    puts("Badluck! There is no flag");
  }
  return 0;
}
```

只看前面还以为有壳，乱七八糟的，直到看到字符串才打消疑虑。逆向现在摆烂了，粗略看一波看不出来大概的逻辑就翻[wp](https://blog.csdn.net/weixin_45055269/article/details/106157485)。原来这是个[多线程](https://zhuanlan.zhihu.com/p/97418361)，特征就是开始的pthread_create等函数。根据函数的签名：

```c
int pthread_create(pthread_t *tidp,const pthread_attr_t *attr, 
                   (void*)(*start_rtn)(void*),void *arg);
```

第一个参数为指向线程标识符的指针。

第二个参数用来设置线程属性。

第三个参数是线程运行函数的起始地址。

最后一个参数是运行函数的参数。

看看start_routine是啥。

```c
void start_routine(int param_1)

{
  long in_FS_OFFSET;
  long md5_result [3];
  long local_20;
  
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  usleep((&DAT_006021f0)[param_1]);
  pthread_mutex_lock((pthread_mutex_t *)&DAT_006021c0);
  md5((long)&DAT_00602180 + (long)(param_1 << 2),4,md5_result);
  if (md5_result[0] == *(long *)(&md5Value + (long)param_1 * 8)) {
    *(undefined4 *)(&flag + count * 4) = *(undefined4 *)((long)&DAT_00602180 + (long)(param_1 << 2))
    ;
  }
  else {
    *(undefined4 *)(&flag + count * 4) = 0;
  }
  count = count + 1;
  pthread_mutex_unlock((pthread_mutex_t *)&DAT_006021c0);
  if (local_20 == *(long *)(in_FS_OFFSET + 0x28)) {
    return;
  }
                    /* WARNING: Subroutine does not return */
  __stack_chk_fail();
}
```

有几个没见过的函数。[usleep](https://blog.csdn.net/whatday/article/details/108942583)挂起进程，单位是微秒。pthread_mutex_lock和pthread_mutex_unlock是配套的，都是c语言里的[互斥锁](https://blog.csdn.net/google19890102/article/details/62047798)，主要功能在于防止不同线程访问同一资源时出现混乱。md5函数不是原生的，是我根据函数里面的实现和wp（当然主要是后面这个:-D）重命名的。

结合main函数中的调用：

```c
__arg = (void *)0x0;
  __newthread = &DAT_00602260;
  do {
    iVar2 = pthread_create(__newthread,(pthread_attr_t *)0x0,start_routine,__arg);
    if (iVar2 != 0) {
      perror("pthread_create");
                    /* WARNING: Subroutine does not return */
      exit(-1);
    }
    __arg = (void *)((long)__arg + 1);
    __newthread = __newthread + 1;
  } while (__arg != (void *)0x6);
```

传入的参数从0开始，一直到6结束，应该一共会创建6个线程。参数用于决定DAT_006021f0的取值，从而决定当前线程挂起多久。回到start_routine函数，最开始不懂DAT_00602180是啥，我们的ghidra再次不负众望，没有反编译出scanf的参数。联系wp和猜测感觉和输入有关，这也算经验吧，这个参数没有往里面传输入相关的参数，却有明显的判断逻辑，说明涉及的值每次都会变。最有可能和输入有关系，那程序里只剩下DAT_00602180了。函数将我们的输入以4个为一组（因为param_1 << 2这句得到的结果是4的倍数），md5加密后和md5Value比对，正确就放到flag里，错误就什么也不放。肯定要正确了，爆破一下。

```python
import hashlib
check="4746bbbd02bb590fbeac2821ece8fc5cad749265ca7503ef4386b38fc12c4227b03ecc45a7ec2da7be3c5ffe121734e8"
for w in range(0,6):
	for i in range(48,123):
		for j in range(48,123):
			for m in range(48,123):
				for n in range(48,123):
					temp=chr(i)+chr(j)+chr(m)+chr(n)
					hashvalue=hashlib.md5(temp.encode()).hexdigest()
					if hashvalue[0:16]==check[w*16:w*16+16]:
						print(w,temp)
```

得到字符串juhuhfenlapsiuerhjifdunu。还有个问题，这里得到的字符串并不是程序实际传入的字符串，因为程序将其4个为一组，然后开线程，每个线程都有延迟和互斥锁，还要看看这些字符串的顺序。最后发现是juhuhfenlapsdunuhjifiuer，不知道怎么得到的，看官方wp可能是爆破。看看exp。

```python
input1='juhuhfenlapsiuerhjifdunu'
check=[0xfe,0xe9,0xf4,0xe2,0xf1,0xfa,0xf4,0xe4,0xf0,0xe7,0xe4,0xe5,0xe3,0xf2,0xf5,0xef,0xe8,0xff,0xf6,0xf4,0xfd,0xb4,0xa5,0xb2]
len=24
i=0
v11=0
while(i!=len):
	v12=ord(input1[i])+i
	v11=v11^v12
	i=i+1

input2='juhuhfenlapsdunuhjifiuer'
flag=''
for i in range(24):
	temp=ord(input2[i])^v11^check[i]
	flag+=chr(temp)
print(flag)
```

第一个while循环其实是main函数里面的这个部分，在开线程之前。

```c
bVar11 = 0;
  for (lVar6 = 0; (long)puVar9 + (-0x602183 - (ulong)CARRY1((byte)uVar4,(byte)uVar4)) != lVar6;
      lVar6 = lVar6 + 1) {
    bVar11 = bVar11 ^ (char)lVar6 + *(char *)((long)&DAT_00602180 + lVar6);
  }
```

你问我奇奇怪怪的那些数字和函数是什么？答案是我也不知道，而且没啥用，bVar11是v11，lVar6是i，DAT_00602180是input1，忽略for循环的条件都是对的。flag在下面的for循环得出，指代main函数里的这个部分：

```c
(&flag)[uVar10] = (&flag)[uVar10] ^ (&DAT_006020e0)[uVar10] ^ bVar11;
    uVar10 = uVar10 + 1;
```

uVar10是索引i。这么看逻辑都是没错且很清晰的，只是多线程有点吓人。

## Flag
> goodjobyougetthisflag233