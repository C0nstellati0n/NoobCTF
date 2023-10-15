# ABC

用numpy.matmul按顺序把A，B和C三个矩阵乘起来即可。结果是一个包含-1和1（浮点数，发现取出来有点误差）的矩阵。将-1看成黑色，1看成白色然后PIL画出二维码即可。

```py
from PIL import Image
import numpy as np
a = np.load('A.npy')
b = np.load('B.npy')
c = np.load('C.npy')
d=np.matmul(a,np.matmul(b,c))
width=len(d)
height=len(d[0])
pic = Image.new("RGB",(width, height))
for y in range (0,height):
	for x in range (0,width):
		if(1-d[y][x]>1):
			pic.putpixel([x,y],(0, 0, 0))
		else:
			pic.putpixel([x,y],(255,255,255))
pic.save("flag.png")
```

二维码扫描： https://zxing.org/w/decode ，似乎不是所有的在线网站都能扫出来