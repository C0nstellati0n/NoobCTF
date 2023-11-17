# Cryptography I

看到有人推荐这个课程我就来了： https://www.coursera.org/learn/crypto 。那么按照我的传统，自然是要写个笔记

## Discrete Probability (Crash Course)

这里教授只是稍微讲一下基础，更详细的内容参考 https://en.wikibooks.org/wiki/High_School_Mathematics_Extensions/Discrete_Probability

离散概率（Discrete Probability）通常定义于一个universe（不太懂怎么翻译），记做U。这里通常为有限集合，例如 $U=\{0,1\}^2=\{00,01,10,11\}$

U上的概率分布（probability distribution）定义为U上函数P，给universe中的每个元素赋值一个0到1之间的数字，这个数字称为该元素的权重（weight）或概率。函数P的唯一限制为 $\Sigma_{x\in U}P(x)=1$

例子：
1. 均匀分布(uniform distribution): $\forall x\in U,P(x)=\frac{1}{|U|},|U|$ 表示U中元素的的数量，或者说U的大小
2. $x_0$ 点处的点分布（point distribution）： $P(x_0)=1,\forall x\not ={x_0},P(x)=0$

因为U是个有限集合，所以可以将集合中所有元素的权重放到一个向量里，称为分布向量（distribution vector）： $(P(x_0),P(x_1),...,P(x_n))$

考虑子集（subset） $A\subseteq U$ ,定义A的权重为A中所有元素权重之和： $Pr[A]=\Sigma_{x\in A}P(x)\in[0,1]$ 。自然Pr[U]=1. 这个子集A叫做事件（event），Pr[A]称为该事件的概率

The union bound: 对于U中两个事件 $A_1$ 和 $A_2$ ，有 $Pr[A_1\cup A_2]\leq Pr[A_1]+Pr[A_2]$ 。当两个事件的并集为空集时，等号成立

随机变量（Random Variables）：一个随机变量X定义为函数 $X:U\rightarrow V$ 。该函数从universe映射到集合V，V是随机变量取值的地方。例如 $X:\{0,1\}^n\rightarrow\{0,1\}$ ，随机变量可能的值为0或1

均匀随机变量（uniform random variable）:定义U为某个有限集合，记 $r\leftarrow^R U$ 为U上的一个均匀随机变量。 $\forall a\in U,Pr[r=a]=\frac{1}{|U|}$ 。正式地说，r为恒等函数（identity function）， $r(x)=a,\forall x\in U$

随机算法(randomized algorithm):确定算法（deterministic algorithm）定义为 $y\leftarrow A(m)$ ，也就是一个输入永远映射到一个输出。而随机算法的定义则是 $y\leftarrow A(m;r)$ ，其中 $r\leftarrow^R\{0,1\}^n$ ，每次算法运行时都会重新采样。因此每次运行函数时，即使输入相同，也会因为不同的r得到不同的输出