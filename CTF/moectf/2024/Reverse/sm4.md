# sm4

题目给了decode函数和密文那就好办了，直接上x64dbg，在decode这里下个断点，把encode_result换成期望密文即可（windows函数调用参数的传递：RCX, RDX, R8, R9）。注意输入任意明文时长度一定要是48，如果小于这个数的话，解密时用的key不对。似乎是48的长度会把key的一个字节覆盖掉，覆盖后才是真正的key