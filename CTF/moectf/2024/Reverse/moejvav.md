# moejvav

```py
instuctions=#可通过反编译jar包得到
index=0
store=0
array=[0]*44
flag=""
prev=[]
while index<len(instuctions):
  inst=instuctions[index]
  index+=1
  if inst==0:
      prev=[]
      print("read from array[0]")
      store=array[0]
      print(f"{store=}")
      print("remove array[0]")
      array.pop(0)
  elif inst==1:
    prev.append(["xor",instuctions[index]])
    print(f"store^=instuctions[{index}]({instuctions[index]})")
    store^=instuctions[index]
    print(f"{store=}")
    index+=1
  elif inst==2:
    prev.append(["plus",instuctions[index]])
    print(f"store+=instuctions[{index}]({instuctions[index]})")
    store += instuctions[index]
    print(f"{store=}")
    index+=1
  elif inst==6:
    print(f"store==instuctions[{index}]({instuctions[index]}): {store==instuctions[index]}")
    value=instuctions[index]
    for i in range(len(prev)-1,-1,-1):
      if prev[i][0]=="xor":
        value^=prev[i][1]
      elif prev[i][0]=="plus":
        value-=prev[i][1]
    flag+=chr(((value-32)^202)&0xff)
    index+=1
print(flag)
```