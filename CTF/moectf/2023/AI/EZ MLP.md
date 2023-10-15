# EZ MLP

运行脚本得到ValueError: matmul: Input operand 1 has a mismatch in its core dimension 0, with gufunc signature (n?,k),(k,m?)->(n?,m?) (size 4 is different from 1)

脚本中只有fc函数使用了matmul，交换weight和x即可