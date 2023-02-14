# universal

[Problem](https://github.com/uclaacm/lactf-archive/tree/main/2023/rev/universal)

Files with ".class" suffix can be opened with [jadx](https://github.com/skylot/jadx).

```java
package p000;
import java.nio.charset.Charset;
import java.util.Scanner;
/* renamed from: FlagChecker */
/* loaded from: FlagChecker.class */
class FlagChecker {
    FlagChecker() {
    }
    public static void main(String[] strArr) {
        System.out.print("What's the flag? ");
        System.out.flush();
        Scanner scanner = new Scanner(System.in);
        String nextLine = scanner.nextLine();
        scanner.close();
        byte[] bytes = nextLine.getBytes(Charset.forName("UTF-8"));
        if (bytes.length == 38 && (((bytes[34] ^ (bytes[23] * 7)) ^ ((bytes[36] ^ (-1)) + 13)) & 255) == 182 && (((bytes[37] ^ (bytes[10] * 7)) ^ ((bytes[21] ^ (-1)) + 13)) & 255) == 223 && (((bytes[24] ^ (bytes[23] * 7)) ^ ((bytes[19] ^ (-1)) + 13)) & 255) == 205 && (((bytes[25] ^ (bytes[13] * 7)) ^ ((bytes[23] ^ (-1)) + 13)) & 255) == 144 && (((bytes[6] ^ (bytes[27] * 7)) ^ ((bytes[25] ^ (-1)) + 13)) & 255) == 138 && (((bytes[4] ^ (bytes[32] * 7)) ^ ((bytes[22] ^ (-1)) + 13)) & 255) == 227 && (((bytes[25] ^ (bytes[19] * 7)) ^ ((bytes[1] ^ (-1)) + 13)) & 255) == 107 && (((bytes[22] ^ (bytes[7] * 7)) ^ ((bytes[29] ^ (-1)) + 13)) & 255) == 85 && (((bytes[15] ^ (bytes[10] * 7)) ^ ((bytes[20] ^ (-1)) + 13)) & 255) == 188 && (((bytes[29] ^ (bytes[16] * 7)) ^ ((bytes[12] ^ (-1)) + 13)) & 255) == 88 && (((bytes[35] ^ (bytes[4] * 7)) ^ ((bytes[33] ^ (-1)) + 13)) & 255) == 84 && (((bytes[36] ^ (bytes[2] * 7)) ^ ((bytes[4] ^ (-1)) + 13)) & 255) == 103 && (((bytes[26] ^ (bytes[3] * 7)) ^ ((bytes[1] ^ (-1)) + 13)) & 255) == 216 && (((bytes[12] ^ (bytes[6] * 7)) ^ ((bytes[18] ^ (-1)) + 13)) & 255) == 165 && (((bytes[12] ^ (bytes[28] * 7)) ^ ((bytes[36] ^ (-1)) + 13)) & 255) == 151 && (((bytes[20] ^ (bytes[0] * 7)) ^ ((bytes[21] ^ (-1)) + 13)) & 255) == 101 && (((bytes[27] ^ (bytes[36] * 7)) ^ ((bytes[14] ^ (-1)) + 13)) & 255) == 248 && (((bytes[35] ^ (bytes[2] * 7)) ^ ((bytes[19] ^ (-1)) + 13)) & 255) == 44 && (((bytes[13] ^ (bytes[11] * 7)) ^ ((bytes[33] ^ (-1)) + 13)) & 255) == 242 && (((bytes[33] ^ (bytes[11] * 7)) ^ ((bytes[3] ^ (-1)) + 13)) & 255) == 235 && (((bytes[31] ^ (bytes[37] * 7)) ^ ((bytes[29] ^ (-1)) + 13)) & 255) == 248 && (((bytes[1] ^ (bytes[33] * 7)) ^ ((bytes[31] ^ (-1)) + 13)) & 255) == 33 && (((bytes[34] ^ (bytes[22] * 7)) ^ ((bytes[35] ^ (-1)) + 13)) & 255) == 84 && (((bytes[36] ^ (bytes[16] * 7)) ^ ((bytes[4] ^ (-1)) + 13)) & 255) == 75 && (((bytes[8] ^ (bytes[3] * 7)) ^ ((bytes[10] ^ (-1)) + 13)) & 255) == 214 && (((bytes[20] ^ (bytes[5] * 7)) ^ ((bytes[12] ^ (-1)) + 13)) & 255) == 193 && (((bytes[28] ^ (bytes[34] * 7)) ^ ((bytes[16] ^ (-1)) + 13)) & 255) == 210 && (((bytes[3] ^ (bytes[35] * 7)) ^ ((bytes[9] ^ (-1)) + 13)) & 255) == 205 && (((bytes[27] ^ (bytes[22] * 7)) ^ ((bytes[2] ^ (-1)) + 13)) & 255) == 46 && (((bytes[27] ^ (bytes[18] * 7)) ^ ((bytes[9] ^ (-1)) + 13)) & 255) == 54 && (((bytes[3] ^ (bytes[29] * 7)) ^ ((bytes[22] ^ (-1)) + 13)) & 255) == 32 && (((bytes[24] ^ (bytes[4] * 7)) ^ ((bytes[13] ^ (-1)) + 13)) & 255) == 99 && (((bytes[22] ^ (bytes[16] * 7)) ^ ((bytes[13] ^ (-1)) + 13)) & 255) == 108 && (((bytes[12] ^ (bytes[8] * 7)) ^ ((bytes[30] ^ (-1)) + 13)) & 255) == 117 && (((bytes[25] ^ (bytes[27] * 7)) ^ ((bytes[35] ^ (-1)) + 13)) & 255) == 146 && (((bytes[16] ^ (bytes[10] * 7)) ^ ((bytes[14] ^ (-1)) + 13)) & 255) == 250 && (((bytes[21] ^ (bytes[25] * 7)) ^ ((bytes[12] ^ (-1)) + 13)) & 255) == 195 && (((bytes[26] ^ (bytes[10] * 7)) ^ ((bytes[30] ^ (-1)) + 13)) & 255) == 203 && (((bytes[20] ^ (bytes[2] * 7)) ^ ((bytes[1] ^ (-1)) + 13)) & 255) == 47 && (((bytes[34] ^ (bytes[12] * 7)) ^ ((bytes[27] ^ (-1)) + 13)) & 255) == 121 && (((bytes[19] ^ (bytes[34] * 7)) ^ ((bytes[20] ^ (-1)) + 13)) & 255) == 246 && (((bytes[25] ^ (bytes[22] * 7)) ^ ((bytes[14] ^ (-1)) + 13)) & 255) == 61 && (((bytes[19] ^ (bytes[28] * 7)) ^ ((bytes[37] ^ (-1)) + 13)) & 255) == 189 && (((bytes[24] ^ (bytes[9] * 7)) ^ ((bytes[17] ^ (-1)) + 13)) & 255) == 185) {
            System.out.println("Correct!");
        } else {
            System.out.println("Not quite...");
        }
    }
}
```

The program checks the flag with a very complicated if statement. This type of question is a classic question type solved using z3. If you are new to z3, try running "pip3 install z3-solver" or "pip install z3-solver" to install it on Python.

```python
from string import ascii_lowercase, ascii_uppercase
from z3 import *
table=ascii_uppercase+ascii_lowercase
st="(((bytes[34] ^ (bytes[23] * 7)) ^ ((bytes[36] ^ (-1)) + 13)) & 255) == 182 && (((bytes[37] ^ (bytes[10] * 7)) ^ ((bytes[21] ^ (-1)) + 13)) & 255) == 223 && (((bytes[24] ^ (bytes[23] * 7)) ^ ((bytes[19] ^ (-1)) + 13)) & 255) == 205 && (((bytes[25] ^ (bytes[13] * 7)) ^ ((bytes[23] ^ (-1)) + 13)) & 255) == 144 && (((bytes[6] ^ (bytes[27] * 7)) ^ ((bytes[25] ^ (-1)) + 13)) & 255) == 138 && (((bytes[4] ^ (bytes[32] * 7)) ^ ((bytes[22] ^ (-1)) + 13)) & 255) == 227 && (((bytes[25] ^ (bytes[19] * 7)) ^ ((bytes[1] ^ (-1)) + 13)) & 255) == 107 && (((bytes[22] ^ (bytes[7] * 7)) ^ ((bytes[29] ^ (-1)) + 13)) & 255) == 85 && (((bytes[15] ^ (bytes[10] * 7)) ^ ((bytes[20] ^ (-1)) + 13)) & 255) == 188 && (((bytes[29] ^ (bytes[16] * 7)) ^ ((bytes[12] ^ (-1)) + 13)) & 255) == 88 && (((bytes[35] ^ (bytes[4] * 7)) ^ ((bytes[33] ^ (-1)) + 13)) & 255) == 84 && (((bytes[36] ^ (bytes[2] * 7)) ^ ((bytes[4] ^ (-1)) + 13)) & 255) == 103 && (((bytes[26] ^ (bytes[3] * 7)) ^ ((bytes[1] ^ (-1)) + 13)) & 255) == 216 && (((bytes[12] ^ (bytes[6] * 7)) ^ ((bytes[18] ^ (-1)) + 13)) & 255) == 165 && (((bytes[12] ^ (bytes[28] * 7)) ^ ((bytes[36] ^ (-1)) + 13)) & 255) == 151 && (((bytes[20] ^ (bytes[0] * 7)) ^ ((bytes[21] ^ (-1)) + 13)) & 255) == 101 && (((bytes[27] ^ (bytes[36] * 7)) ^ ((bytes[14] ^ (-1)) + 13)) & 255) == 248 && (((bytes[35] ^ (bytes[2] * 7)) ^ ((bytes[19] ^ (-1)) + 13)) & 255) == 44 && (((bytes[13] ^ (bytes[11] * 7)) ^ ((bytes[33] ^ (-1)) + 13)) & 255) == 242 && (((bytes[33] ^ (bytes[11] * 7)) ^ ((bytes[3] ^ (-1)) + 13)) & 255) == 235 && (((bytes[31] ^ (bytes[37] * 7)) ^ ((bytes[29] ^ (-1)) + 13)) & 255) == 248 && (((bytes[1] ^ (bytes[33] * 7)) ^ ((bytes[31] ^ (-1)) + 13)) & 255) == 33 && (((bytes[34] ^ (bytes[22] * 7)) ^ ((bytes[35] ^ (-1)) + 13)) & 255) == 84 && (((bytes[36] ^ (bytes[16] * 7)) ^ ((bytes[4] ^ (-1)) + 13)) & 255) == 75 && (((bytes[8] ^ (bytes[3] * 7)) ^ ((bytes[10] ^ (-1)) + 13)) & 255) == 214 && (((bytes[20] ^ (bytes[5] * 7)) ^ ((bytes[12] ^ (-1)) + 13)) & 255) == 193 && (((bytes[28] ^ (bytes[34] * 7)) ^ ((bytes[16] ^ (-1)) + 13)) & 255) == 210 && (((bytes[3] ^ (bytes[35] * 7)) ^ ((bytes[9] ^ (-1)) + 13)) & 255) == 205 && (((bytes[27] ^ (bytes[22] * 7)) ^ ((bytes[2] ^ (-1)) + 13)) & 255) == 46 && (((bytes[27] ^ (bytes[18] * 7)) ^ ((bytes[9] ^ (-1)) + 13)) & 255) == 54 && (((bytes[3] ^ (bytes[29] * 7)) ^ ((bytes[22] ^ (-1)) + 13)) & 255) == 32 && (((bytes[24] ^ (bytes[4] * 7)) ^ ((bytes[13] ^ (-1)) + 13)) & 255) == 99 && (((bytes[22] ^ (bytes[16] * 7)) ^ ((bytes[13] ^ (-1)) + 13)) & 255) == 108 && (((bytes[12] ^ (bytes[8] * 7)) ^ ((bytes[30] ^ (-1)) + 13)) & 255) == 117 && (((bytes[25] ^ (bytes[27] * 7)) ^ ((bytes[35] ^ (-1)) + 13)) & 255) == 146 && (((bytes[16] ^ (bytes[10] * 7)) ^ ((bytes[14] ^ (-1)) + 13)) & 255) == 250 && (((bytes[21] ^ (bytes[25] * 7)) ^ ((bytes[12] ^ (-1)) + 13)) & 255) == 195 && (((bytes[26] ^ (bytes[10] * 7)) ^ ((bytes[30] ^ (-1)) + 13)) & 255) == 203 && (((bytes[20] ^ (bytes[2] * 7)) ^ ((bytes[1] ^ (-1)) + 13)) & 255) == 47 && (((bytes[34] ^ (bytes[12] * 7)) ^ ((bytes[27] ^ (-1)) + 13)) & 255) == 121 && (((bytes[19] ^ (bytes[34] * 7)) ^ ((bytes[20] ^ (-1)) + 13)) & 255) == 246 && (((bytes[25] ^ (bytes[22] * 7)) ^ ((bytes[14] ^ (-1)) + 13)) & 255) == 61 && (((bytes[19] ^ (bytes[28] * 7)) ^ ((bytes[37] ^ (-1)) + 13)) & 255) == 189 && (((bytes[24] ^ (bytes[9] * 7)) ^ ((bytes[17] ^ (-1)) + 13)) & 255) == 185"
""" for i in range(38):
    print(f"{table[i]}=BitVec('{table[i]}',8)") """ #I use these codes to generate the variable declaration below, and if I use eval, an error will be reported. The purpose of choosing regular letters as variable names is to output the sorting results later.
A=BitVec('A',8) #BitVec declares a bit vector. The first parameter should be consistent with the variable name, and the second parameter is the number of digits. 8 bits are selected here, which is enough to express all visible characters. Int can be used directly for general mathematical operations, but here there are bit operations XOR, only BitVec can be used.
B=BitVec('B',8)
C=BitVec('C',8)
D=BitVec('D',8)
E=BitVec('E',8)
F=BitVec('F',8)
G=BitVec('G',8)
H=BitVec('H',8)
I=BitVec('I',8)
J=BitVec('J',8)
K=BitVec('K',8)
L=BitVec('L',8)
M=BitVec('M',8)
N=BitVec('N',8)
O=BitVec('O',8)
P=BitVec('P',8)
Q=BitVec('Q',8)
R=BitVec('R',8)
S=BitVec('S',8)
T=BitVec('T',8)
U=BitVec('U',8)
V=BitVec('V',8)
W=BitVec('W',8)
X=BitVec('X',8)
Y=BitVec('Y',8)
Z=BitVec('Z',8)
a=BitVec('a',8)
b=BitVec('b',8)
c=BitVec('c',8)
d=BitVec('d',8)
e=BitVec('e',8)
f=BitVec('f',8)
g=BitVec('g',8)
h=BitVec('h',8)
i=BitVec('i',8)
j=BitVec('j',8)
k=BitVec('k',8)
l=BitVec('l',8)
solver=Solver() #Declare a Solver type variable.
for x in st.split(' && '):
    temp=x
    for y in range(38):
        temp=temp.replace(f"bytes[{y}]",f"{table[y]}")
    eval(f"solver.add({temp})") #Adding constraints to the solver can be roughly understood as filling in the equations, and z3 will try to solve them based on these equations.
if solver.check(): #Check if there's a solution.
    model=solver.model() #If there is, model() will give the solution.
    model=sorted ([(x, model[x]) for x in model], key = lambda x: str(x[0])) #https://stackoverflow.com/questions/70529941/z3-python-ordering-models-and-accessing-their-elements
    for i in range(38):
        print(chr(model[i][1].as_long()),end='') #Use "as_long()" to convert the BitVec to a number.
```

## Flag
> lactf{1_d0nt_see_3_b1ll10n_s0lv3s_y3t}