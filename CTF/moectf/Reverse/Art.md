# Art

这题给我整疑惑了。

我们再次遇到了一个好心的出题人，直接把考点告诉你。运行程序输入f得到下面的内容。

- Do you know UPX???
<Br>Oh no...Something seems to be wrong...My equations has multiple solutions...
<br>May be I can check it by a hash algorithm. You can never reverse it!!!
<br>Input your flag:f
<Br>QwQ. Something wrong. Please try again. >_<

如果直接把程序放入ghidra或者ida进行分析，什么都看不出来。程序直接告诉你了：知道upx不？其实正常反编译文件的先决步骤就是检查程序的壳，防止做无用功。其实也容易分辨，如果直接反编译不脱壳的程序直接连入口都定位不到，里面的函数也很少，看不出用处。ghidra里（不知道ida是不是这样）甚至无法在菜单栏的strings中找到程序中应该有的字符。直接告诉我们是upx壳了就不用检查了，一行命令脱壳。

- upx -d Art.exe

脱壳后的文件会覆盖原文件，大概是因为在同目录下。我最开始还不信邪，选择逆向elf文件，结果真的没法看，反而是exe无比清晰。看来“ghidra反编译elf比exe好”这句话要看情况。

```c
undefined8 Main(void)
{
  bool bVar1;
  int iVar2;
  undefined7 extraout_var;
  byte local_e8 [112];
  byte local_78 [108];
  int i;
  FUN_00402030();
  puts("Do you know UPX???");
  puts("Oh no...Something seems to be wrong...My equations has multiple solutions...");
  puts("May be I can check it by a hash algorithm. You can never reverse it!!!");
  printf("Input your flag:");
  scanf("%s");
  for (i = 0; i < 28; i = i + 1) {
    local_e8[i] = local_78[i];
  }
  for (i = 1; i < 28; i = i + 1) {
    local_78[i + -1] = local_78[i + -1] ^ local_78[i] + (char)local_78[i + -1] % 17 ^ 0x19;
  }
  iVar2 = strcmp((char *)local_78,&DAT_00404020);
  if ((iVar2 == 0) &&
     (bVar1 = FUN_00401550((char *)local_e8), (int)CONCAT71(extraout_var,bVar1) != 0)) {
    puts("\nGood job!!! You know UPX and hash!!!");
    return 0;
  }
  puts("\nQwQ. Something wrong. Please try again. >_<");
  return 0;
}
```

然后我就疑惑了。FUN_00401550大概率是求hash值的。为什么我说大概呢，因为题目里提到了，ghidra反编译出来这个函数非常复杂，我根本看不出来在干啥，只能大胆猜测。疑惑的点在于if判断条件不只有hash，还有一个异或内容，且正确的异或结果我们是知道的，就是DAT_00404020的内容。不过异或逻辑无法逆向，因为同时涉及两个值，那就爆破吧，艺术就是爆炸！

```python
from string import printable
data='02 18 0f f8 19 04 27 d8 eb 00 35 48 4d 2a 45 6b 59 2e 43 01 18 5c 09 09 09 09 b5 7d'
data=data.split(' ')
def encode(first,second):
   return ord(first)^ord(second)+ord(first)%17^0x19
flag='moectf{'
for i in range(6,28):
   current_first=flag[i]
   expected_value=int(data[i],16)
   for letter in printable:
      result=encode(current_first,letter)
      if result==expected_value:
         flag+=letter
         break
print(flag)
```

结果直接出来了。还有这么好的事？hash可能就是个幌子吧。快说谢谢出题人，要不是直接出来了我就要去看ghidra反编译出来的hash算法了，会死人的。

- ### Flag
  > moectf{Art_i5_b14s7ing!!!!!}