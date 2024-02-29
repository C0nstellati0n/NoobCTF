# [Riceboard](https://challenges.reply.com/challenges/coding-teen/teen-edition-code-challenge/detail/)

题目本身很简单，就是找等比数列的和模上一个数。等比数列之和的公式人尽皆知，我最开始也以为这题就是套个公式再模即可。到第四个testcase时出问题了，除法对于较大的数字（本来以为是pow太慢了，看了官方解析后才明白是除法太慢了）过慢，TLE无法避免。既然一切都在模M下进行，直接将除法换成等价的“乘上对应数的模逆元”即可。然后一个新的问题就出现了，要是计算模逆元的两个数之间不互质咋办？是时候该端上来官方解法了（以及个人补充的与testcase交互部分）：
```py
#https://challenges.reply.com/challenges/coding-teen/learn-train/teen-challenge-2019-solution/
def riceboard(R,N,M):
    X=N**2 #要计算的等比数列项数
    powr=[1,R] #R^0和R^1
    sumr=[1,1+R] #三言两语不知道怎么解释，直接看下面的计算最好
    i=1
    while i<X:
        i*=2
        powr.append((powr[-1]*powr[-1])%M) #这块计算R^2,R^4,R^8，存入powr
        #sumr的期望值是R的每个次方的prefix sum，但是上面只计算了2次方的
        sumr.append((((1+powr[-1])%M)*sumr[-1])%M) #所以这里用一点数学，(1+powr[-1])*sumr[-1]=sumr[-1]+powr[-1]*sumr[-1]。为了方便理解，模拟运行前两段while循环：powr[-1]=R,powr后添加powr[-1]*powr[-1]=R^2（注意后面计算sumr时powr[-1]就变成这个了）。sumr添加sumr[-1]+powr[-1]*sumr[-1]=1+R+R^2*(1+R)=1+R+R^2+R^3。第二轮while循环，powr[-1]=R^2,powr后添加powr[-1]*powr[-1]=R^4。sumr添加sumr[-1]+powr[-1]*sumr[-1]=1+R+R^2+R^3+R^4*(1+R+R^2+R^3)=1+R+R^2+R^3+R^4+R^5+R^6+R^7
    mul,S=1,0
    b=bin(X)[2:]
    for i in range(len(b)):
        if b[i]=='0':
            continue
        i=len(b)-i-1 #这块修改了for循环计数变量不要紧，后面range自动修正
        #这两行还是拿官方案例好理解：
        #bin(25)=11001
        #R^0+...+R^24=(R^0+...R^15)+R^16(R^0+...R^7)+(R^16*R^8)*(R^0)
        #括号之前的数就是当前的mul，括号里的内容为sumr[i]
        S=(S+((mul*sumr[i])%M))%M
        mul=(mul*powr[i+1])%M
    return S
def testcase():
    line=input().split(" ")
    R=int(line[0])
    N=int(line[1])
    M=int(line[2])
    return riceboard(R,N,M)
num=int(input())
output=""
for i in range(1,num+1):
    output+=f"Case #{i}: {testcase()}\n"
print(output[:-1])
```