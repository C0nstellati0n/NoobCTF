# zorropub

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=87cd63c0-2b9d-486d-b571-48ca50abdd6c_2)

爆破！

程序中只有main函数有用。

```c
void Main(void)

{
  int iVar1;
  size_t len;
  long in_FS_OFFSET;
  uint numberOfDrinks;
  uint drinkId;
  uint i;
  uint j;
  uint local_fc;
  MD5_CTX local_f8;
  byte local_98 [16];
  byte flag [32];
  char local_68 [32];
  char local_48 [40];
  long local_20;
  
  local_20 = *(long *)(in_FS_OFFSET + 0x28);
  j = 0;
  puts("Welcome to Pub Zorro!!");
  printf("Straight to the point. How many drinks you want?");
  __isoc99_scanf(&%d,&numberOfDrinks);
  if ((int)numberOfDrinks < 1) {
    printf("You are too drunk!! Get Out!!");
                    /* WARNING: Subroutine does not return */
    exit(-1);
  }
  printf("OK. I need details of all the drinks. Give me %d drink ids:",(ulong)numberOfDrinks);
  for (i = 0; (int)i < (int)numberOfDrinks; i = i + 1) {
    __isoc99_scanf(&%d,&drinkId);
    if (((int)drinkId < 0x11) || (0xffff < (int)drinkId)) {
      puts("Invalid Drink Id.");
      printf("Get Out!!");
                    /* WARNING: Subroutine does not return */
      exit(-1);
    }
    j = j ^ drinkId;
  }
  local_fc = 0;
  for (i = j; i != 0; i = i & i - 1) {
    local_fc = local_fc + 1;
  }
  if (local_fc != 10) {
    puts("Looks like its a dangerous combination of drinks right there.");
    puts("Get Out, you will get yourself killed");
                    /* WARNING: Subroutine does not return */
    exit(-1);
  }
  srand(j);
  MD5_Init(&local_f8);
  for (i = 0; (int)i < 30; i = i + 1) {
    iVar1 = rand();
    local_fc = iVar1 % 1000;
    sprintf(local_68,"%d",(ulong)local_fc);
    len = strlen(local_68);
    MD5_Update(&local_f8,local_68,len);
    flag[(int)i] = (byte)*(undefined4 *)(&DAT_006020c0 + (long)(int)i * 4) ^ (byte)local_fc;
  }
  flag[(int)i] = 0;
  MD5_Final(local_98,&local_f8);
  for (i = 0; (int)i < 0x10; i = i + 1) {
    sprintf(local_48 + (int)(i * 2),"%02x",(ulong)local_98[(int)i]);
  }
  iVar1 = strcmp(local_48,"5eba99aff105c9ff6a1a913e343fec67");
  if (iVar1 != 0) {
    puts("Try different mix, This mix is too sloppy");
                    /* WARNING: Subroutine does not return */
    exit(-1);
  }
  printf("\nYou choose right mix and here is your reward: The flag is nullcon{%s}\n",flag);
  if (local_20 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
}
```

分析一下flag的生成。首先输入numberOfDrinks的值，不能小于1。接着输入drinkId，值不能小于0x11或者大于0xffff。每个得到的drinkId与j异或，j初始值是0，相当于输入的drinkId之间异或。然后把j用作srand的种子。最后用这个种子生成的随机数与DAT_006020c0数组的元素进行异或，得到flag。drinkId与随机数的生成有着密切关系，肯定不是所有id都行的。下方还有一个过滤，要求几轮md5加密后生成的值于5eba99aff105c9ff6a1a913e343fec67。我们还只能控制偶数位，因为根据这个for语句：

```c
for (i = 0; (int)i < 0x10; i = i + 1) {
    sprintf(local_48 + (int)(i * 2),"%02x",(ulong)local_98[(int)i]);
  }
```

只对偶数位赋值。这怎么可能逆得出来，直接爆破。

```python
from pwn import*
import time
time1=time.time()
a=[]

for i in range(16,0xffff):
	v9=0
	i=i^0
	j=i
	while(i):
		v9+=1
		i&=i-1
	if v9 ==10:
		a.append(j)

for i in a:
	p=process("./zorropub")
	p.recv()
	p.sendline('1')
	p.sendline(str(i))
	result=p.recv()
	if "null" in text:
		print text
		time2=time.time()
		print("time %fs"%(time2-time1))
		break
p.close()
```

- ### Flag
  > nullcon{nu11c0n_s4yz_x0r1n6_1s_4m4z1ng}