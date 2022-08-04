# Hidden-Message

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=1f460b69-6d7e-423f-8776-5127dfb6e293_2)

附件拿到后发现是个pcap文件。这个文件就是流量捕捉包，立刻放到wireshark中进行分析。出乎意料的是，与其他上万个包的流量分析题不同，这里只有80个包。（右下角）

![packets](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/packets.png)

别看包的数量不多，我在里面找了很久都没有发现任何可疑的东西，只有一篇啥用没有的量子力学短文。

![内容](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/passage.png)

Tips：可以在wireshark的菜单中找到分析（Analyze）->Follow选项中跟踪数据流。很多时候flag或者提示就藏在里面。

读了几遍是啥也没看出来。网上查找后才发现一个细节：发送数据包的端口最后一位在变化。

![端口](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/port.png)

变化的只有0和1，很容易就想到二进制。从Wireshark中到处全部的包方便提取出端口信息。（菜单栏File->Export Packet Dissections->As Json)

![](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/export.png)

然后就可以根据json读取每个包的端口。这里有点绕，先把代码贴出来：
```
import json
import re
result=''
ports=[]
with open("你的json文件绝对路径",'r') as f:
    result=f.read()
result=json.loads(result)
for i in range(len(result)):
    ports.append(result[i]['_source']["layers"]["udp"]['udp.srcport'][-1:])
flag=''
for i in ports:
    print(i)
    if i=='0':
        flag+='1'
    else:
        flag+='0'
print(flag)
```
json.loads()方法可以加载一个json格式的字符串，将其变为真正的json。这里读取出来的结果是一个列表，列表中的每个索引都对应一个包。每个包又是一个字典，而端口就在那一串键下。获取到端口后别忘了切割字符串，只留下最后一位。

后面的for循环是交换结果中0和1的位置。因为刚刚的结果直接拿去做转换是啥也没有的。没有其他思路和提示的情况下就可以考虑将0和1的位置互换。得到的结果放到[CyberChef](https://gchq.github.io/CyberChef/)中就可以看到最后的flag。

![flag](https://github.com/C0nstellati0n/NoobCTF/blob/main/%E6%94%BB%E9%98%B2%E4%B8%96%E7%95%8C/images/cyberchef.png)