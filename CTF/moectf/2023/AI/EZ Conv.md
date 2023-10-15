# EZ Conv

其实是个api题，完全不需要自己去实现卷积。参考 https://www.geeksforgeeks.org/apply-a-2d-convolution-operation-in-pytorch/ 和 https://stackoverflow.com/questions/49768306/pytorch-tensor-to-numpy-array
```py
import torch
import numpy
from PIL import Image
inp=torch.from_numpy(numpy.load("inp.npy"))
w=torch.from_numpy(numpy.load("w.npy"))
b=torch.from_numpy(numpy.load("b.npy"))
print(inp)
def conv(x, w, b):
    c=torch.nn.Conv2d(1, 1, 1,bias=False)
    c.weight=torch.nn.Parameter(w)
    c.bias=torch.nn.Parameter(b)
    return c(x)
def get_25x25_QR_code(x):
    tensor=x.detach().numpy()
    width=height=25
    pic = Image.new("RGB",(width, height))
    x=0
    y=0
    while y<25:
        row=tensor[y]
        for i in range(5):
            for j in range(5):
                if(1-row[i][j]>1):
                    pic.putpixel([x,y],(0, 0, 0))
                else:
                    pic.putpixel([x,y],(255,255,255))
                x+=1
        x=0
        y+=1
    pic.save("flag.png")
get_25x25_QR_code(conv(inp,w,b))
```