# CrackRTF

[题目地址](https://buuoj.cn/challenges#CrackRTF)

描述过于生草。

要求输入正确密码。查看main函数内部逻辑发现我们的输入进入`sub_40100A`函数加密后与期望结果进行比对。`sub_40100A`函数内部又调用了一个别的函数，东西不多，重点在CryptCreateHash的第二个参数`0x8004`。查阅[官方文档](https://learn.microsoft.com/en-us/openspecs/windows_protocols/mc-mqac/4ce4a6db-776c-48a3-abaa-c8d7e082f0f8)，发现是sha1。那么直接爆破，因为main函数里面`atoi`限制了输入是数字且大于10000，爆破空间不大。

```python
import hashlib

flag = "@DBApp"

for i in range(100000,999999):
	s = str(i)+flag
	x = hashlib.sha1(s.encode())
	cnt = x.hexdigest()
	if "6e32d0943418c2c" in cnt:
		print(cnt)
		print(str(i)+flag)
```

得到第一个密码为`123321`。然后到第二个密码，差不多一个套路，把输入放进加密函数`sub_401019`后拼接进行比对。加密函数内部构造和刚才的差不多，只不过这次CryptCreateHash的第二个参数变成了0x8003。参照上面的文档是md5，然而这回没有输入内容的限制，难以爆破。反正刚刚那个脚本也是[wp](https://blog.csdn.net/qq_42967398/article/details/96492843)找的，继续看一下思路是什么也行（摆大烂）。

仔细看会发现if语句判断后还有一个附加判断，把内容限制放到了下面，迷惑像我一样的萌新。`sub_40100F`的参数是`第二次密码+123321"@DBApp`,之后可能会用。内部套了几层娃调用了这个函数：

这个函数里a2是写入的目标，lpString是刚才的参数，a3是长度。这个逻辑很明显是个异或，然而异或操作数和结果都不知道。往回推两层，在`sub_4014d0`中发现调用了FindResourceA的一个参数叫AAA。肯定不是乱写的，程序运行时肯定有一个资源叫AAA。用Resource Hacker得到资源内容，取出前6个字节就是异或操作数了。还差个异或结果。继续往下看，`sub_4014d0`后面调用了[WriteFile](https://blog.csdn.net/qq_41476542/article/details/102835162)往`dbapp.rtf`里写入刚刚异或内容，而且是写入开头。rtf文件有固定文件头`{\rtf1\ansi\ansicpg936\deff0\deflang1033等等等`，那取出前6位就是异或结果了。现在即可复原密码。

```python
s = "{\\rtf1"

a = [0x05,0x7D,0x41,0x15,0x26,0x01]

flag = ""
for i in range(0,len(s)):
	x = ord(s[i]) ^ a[i]
	flag += chr(x)
print(flag)
```

两次密码输入正确好运行程序即可在运行目录下得到一个rtf文件，里面就是flag。

## Flag
> flag{N0_M0re_Free_Bugs}