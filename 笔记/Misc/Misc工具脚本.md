# Misc工具脚本

有时候一个知道的知识点却不记得解题脚本放哪个wp里了，又懒得再写一遍。那就专门开个地方存起来。

## Base64隐写

[来源](https://zhuanlan.zhihu.com/p/349481870)

```python
import base64

def Base64Stego_Decrypt(LineList):
    Base64Char = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"     #Base64字符集 已按照规范排列
    BinaryText = ""
    for line in LineList:
        if line.find("==") > 0:     #如果文本中有2个=符号
            temp = bin(Base64Char.find(line[-3]) & 15)[2:]      #通过按位与&15运算取出二进制数后4位 [2:]的作用是将0b过滤掉
            BinaryText = BinaryText+"0"*(4-len(temp))+temp      #高位补0
        elif line.find("=") > 0:        #如果文本中有1个=符号
            temp = bin(Base64Char.find(line[-2]) & 3)[2:]       #通过按位与&3运算取出二进制数后2位
            BinaryText = BinaryText+"0"*(2-len(temp))+temp      #高位补0
    Text = ""
    if(len(BinaryText) % 8 != 0):       #最终得到的隐写数据二进制位数不一定都是8的倍数，为了避免数组越界，加上一个判断
        print("警告:二进制文本位数有误，将进行不完整解析。")
        for i in range(0, len(BinaryText), 8):
            if(i+8 > len(BinaryText)):
                Text = Text+"-"+BinaryText[i:]
                return Text
            else:
                Text = Text+chr(int(BinaryText[i:i+8], 2))
    else:
        for i in range(0, len(BinaryText), 8):
            Text = Text+chr(int(BinaryText[i:i+8], 2))      #将得到的二进制数每8位一组对照ASCII码转化字符
        return Text

def Base64_ForString_Decrypt(Text):     #Base64解密
    try:
        DecryptedText = str(Text).encode("utf-8")
        DecryptedText = base64.b64decode(DecryptedText)
        DecryptedText = DecryptedText.decode("utf-8")
    except:
        return 0
    return DecryptedText

if __name__ == "__main__":
    Course = input("文件名:")
    File = open(Course, "r")
    LineList = File.read().splitlines()
    print("显式内容为:")
    for line in LineList:
        print(Base64_ForString_Decrypt(line),end="")
    print("\n隐写内容为:")
    print(Base64Stego_Decrypt(LineList))
```