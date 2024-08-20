# [Baby Bundle](https://github.com/idekctf/idekctf-2024/tree/main/crypto/baby-bundle)

这段时间都没有好好看数学，已经对数学ptsd了，各种wp里的长篇大论看着就头痛（不记得在哪里看到的这句话：“数学论文分两种，一种是看了第一页就不想看的，另一种是看了第一行就不想看的”）。今天想好好看一篇，结果一脚踩进了坑里——这是英文吗？怎么一个字没看懂？遂专门写一篇文章控告数学……（其实是对wp里我看不懂的句子进行批注。知识点来自chatgpt，所以可能有错的）

- Let $X=\mathbb P^1_F$ . What is the function field $K(X)$ of $X$?

$\mathbb P^1_F$ 指域F上的射影线(projective line over a field),是射影空间（projective space） $\mathbb P^n_F$ 的特例（n=1）。射影空间 $\mathbb P^n_F$ 又指n+1维空间 $F^{n+1}$ 里所有经过原点的线的集合。换句话说，是 $F^{n+1}$ 里所有非零向量的等价类 $(x_0​,x_1​,…,x_n​)$ 的集合。两个向量间的等价关系定义为： $(x_0​:x_1​:…:x_n​)∼(\lambda x_0​:\lambda x_1​:…:\lambda x_n​),\lambda\in F,\lambda\not ={0}$ ,即只要向量B是向量A的非零标量倍，两者就是相等的（诶，配合下面维基百科给出的图，这里的等价类代表的是不是“平行”？两条线若相交于无穷远点就将两者看成是相等的，因此那个标量代表把一条线平移？）。每个等价类称为一个齐次坐标（homogeneous coordinate）。插一嘴，查了[维基百科](https://en.wikipedia.org/wiki/Projective_space)，里面的定义好像有点不太一样，似乎没有明确提到第一个定义里的“相交于原点”？它只说是“set of the vector lines”。呃，先记定义吧，又是一个“xxx的集合”

回到射影线。chatgpt说其实是仿射线（affine line）加个无穷远点，仿射线就更简单了，只是代表平时看到的最简单的线而已。你这么说我可就要明白了啊（