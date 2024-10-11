# moeprotector

完全靠动调做的这题……ghidra倒是能看到SEH部分的伪代码，然而实在是太难懂了，所有SSE xmm系列指令的反编译结果混成一团，甚至没有汇编好理解

于是上动调。还好可以从汇编的长度知道加密逻辑并不复杂，给了我足够的信心硬着头皮跟下来。也就是繁琐了些，一个一个看异或的值，绕过调试器检查之类的
```py
values="""flag[:4]^=0x18171615
flag[:4]+=0x14141414
flag[4:8]^=0x1c1b1a19
flag[4:8]+=0x14141414
flag[8:12]^=0x201f1e1d
flag[8:12]+=0x14141414
flag[12:16]^=0x24232221
flag[12:16]+=0x14141414
flag[16:20]^=0x28272625
flag[16:20]+=0x14141414
flag[20:24]^=0x2c2b2a29
flag[20:24]+=0x14141414
flag[24:28]^=0x302f2e2d
flag[24:28]+=0x14141414
flag[28:32]^=0x34333231
flag[28:32]+=0x14141414
flag[32:36]^=0x38373635
flag[32:36]+=0x14141414
flag[36:40]^=0x3c3b3a39
flag[36:40]+=0x14141414
flag[40:44]^=0x403f3e3d
flag[40:44]+=0x14141414
flag[44:48]^=0x44434241
flag[44:48]+=0x14141414
flag[48:52]^=0x48474645
flag[48:52]+=0x14141414
flag[52:56]^=0x4c4b4a49
flag[52:56]+=0x14141414
flag[:4]^=0x1d1c1b1a
flag[:4]+=0x14141414
flag[4:8]^=0x21201f1e
flag[4:8]+=0x14141414
flag[8:12]^=0x25242322
flag[8:12]+=0x14141414
flag[12:16]^=0x29282726
flag[12:16]+=0x14141414
flag[16:20]^=0x2d2c2b2a
flag[16:20]+=0x14141414
flag[20:24]^=0x31302f2e
flag[20:24]+=0x14141414
flag[24:28]^=0x35343332
flag[24:28]+=0x14141414
flag[28:32]^=0x39383736
flag[28:32]+=0x14141414
flag[32:36]^=0x3d3c3b3a
flag[32:36]+=0x14141414
flag[36:40]^=0x41403f3e
flag[36:40]+=0x14141414
flag[40:44]^=0x45444342
flag[40:44]+=0x14141414
flag[44:48]^=0x49484746
flag[44:48]+=0x14141414
flag[48:52]^=0x4d4c4b4a
flag[48:52]+=0x14141414
flag[52:56]^=0x51504f4e
flag[52:56]+=0x14141414
flag[:4]^=0x1c1b1a19
flag[:4]+=0x14141414
flag[4:8]^=0x201f1e1d
flag[4:8]+=0x14141414
flag[8:12]^=0x24232221
flag[8:12]+=0x14141414
flag[12:16]^=0x28272625
flag[12:16]+=0x14141414
flag[16:20]^=0x2c2b2a29
flag[16:20]+=0x14141414
flag[20:24]^=0x302f2e2d
flag[20:24]+=0x14141414
flag[24:28]^=0x34333231
flag[24:28]+=0x14141414
flag[28:32]^=0x38373635
flag[28:32]+=0x14141414
flag[32:36]^=0x3c3b3a39
flag[32:36]+=0x14141414
flag[36:40]^=0x403f3e3d
flag[36:40]+=0x14141414
flag[40:44]^=0x44434241
flag[40:44]+=0x14141414
flag[44:48]^=0x48474645
flag[44:48]+=0x14141414
flag[48:52]^=0x4c4b4a49
flag[48:52]+=0x14141414
flag[52:56]^=0x504f4e4d
flag[52:56]+=0x14141414""".split("\n")
cipher="c7 c4 c9 ce c2 d1 8b 66 6b 8d b0 45 f9 84 ff b2 51 ab b3 4c 33 a8 61 0e c5 3b 5b f9 11 82 8b 8e 7a 23 68 7a 21 1f 87 91 46 8d 90 a4 a5 e0 35 d9 41 4e 44 f1 37 af 26 3a 8f".split()
curr=""
flag=b""
def decrypt(index,cipher):
    index=index+2*28
    for i in range(3):
        cipher-=0x14141414
        cipher^=int(values[index].split("^=")[1],16)
        index-=28
    return hex(cipher)[2:]
index=0
for i in range(0,len(cipher)-1,4):
    curr=cipher[i+3]+cipher[i+2]+cipher[i+1]+cipher[i]
    try:
        flag+=bytes.fromhex(decrypt(index,int(curr,16)))[::-1]
    except:
        print(index)
        print(curr)
        flag+=b"~~~~"
    index+=2
    curr=""
print(flag.replace(b"~~~~",bytes.fromhex(decrypt(10,int("010e61a833",16)))[::-1])+b'}') #蒙的，果然是溢出了一个01
#flag是 moectf{w1Nd0Ws_S3H_15_A_g0oD_m37h0d_70_h4nd13_EXCEPTI0NS} ，不知道为什么程序算出的是n37h0d。不过可以自己看出来错误然后改对
```