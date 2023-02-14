# caterpillar

[Problem](https://github.com/uclaacm/lactf-archive/tree/master/2023/rev/caterpillar)

We got a code with lots of "-~-~-~-~[]". Open the console that comes with Chrome, and I found that the output of "-~-~-~-~[]" is 4. Every time an additional "-~" is added, the number increases by 1. It seems that the number of "-~" is the value of the expression. Then just write a script to calculate the number of "-~".

```python
with open("caterpillar.js") as f:
    d=f.read().split(" && ") #Split the file content according to " && ", and the obtained list contains the comparison conditions of the flag.
table={}
flag=['']*70
for i in d:
    temp=i.split(" == ") #Split each condition according to "==", the front is the position of the flag character, and the back is the flag character.
    key=temp[0].count("-~")
    value=temp[1].count("-~")
    table[key]=value
for i in table.keys():
    flag[i]=chr(table[i])
print(''.join(flag))
```

## Flag
> lactf{th3_hungry_l1ttl3_c4t3rp1ll4r_at3_th3_fl4g_4g41n}