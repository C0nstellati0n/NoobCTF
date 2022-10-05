# Gracias

[题目地址](https://adworld.xctf.org.cn/challenges/details?hash=d0be0c5f-ac48-4889-82b4-bda35fb2be05_2&task_category_id=5)

我不会看和用sagemath。但是题目可不管你那么多，就给你个sage脚本当"题目"。

```python
from sage.all import *
# Original: https://github.com/mimoo/RSA-and-LLL-attacks/blob/master/boneh_durfee.sage

dimension_min = 7

def remove_unhelpful(BB, monomials, bound, current):
  if current == -1 or BB.dimensions()[0] <= dimension_min:
    return BB
  for ii in range(current, -1, -1):
    if BB[ii, ii] >= bound:
      affected_vectors = 0
      affected_vector_index = 0
      for jj in range(ii + 1, BB.dimensions()[0]):
        if BB[jj, ii] != 0:
          affected_vectors += 1
          affected_vector_index = jj
      if affected_vectors == 0:
        #print "* removing unhelpful vector", ii
        BB = BB.delete_columns([ii])
        BB = BB.delete_rows([ii])
        monomials.pop(ii)
        BB = remove_unhelpful(BB, monomials, bound, ii-1)
        return BB
      elif affected_vectors == 1:
        affected_deeper = True
        for kk in range(affected_vector_index + 1, BB.dimensions()[0]):
          if BB[kk, affected_vector_index] != 0:
            affected_deeper = False
        if affected_deeper and abs(bound - BB[affected_vector_index, affected_vector_index]) < abs(bound - BB[ii, ii]):
          #print "* removing unhelpful vectors", ii, "and", affected_vector_index
          BB = BB.delete_columns([affected_vector_index, ii])
          BB = BB.delete_rows([affected_vector_index, ii])
          monomials.pop(affected_vector_index)
          monomials.pop(ii)
          BB = remove_unhelpful(BB, monomials, bound, ii-1)
          return BB
  return BB

def boneh_durfee_small_roots(pol, modulus, mm, tt, XX, YY):
    PR.<u, x, y> = PolynomialRing(ZZ)
    Q = PR.quotient(x*y + 1 - u) # u = xy + 1
    polZ = Q(pol).lift()
    UU = XX*YY + 1
    gg = []
    for kk in range(mm + 1):
      for ii in range(mm - kk + 1):
        xshift = x^ii * modulus^(mm - kk) * polZ(u, x, y)^kk
        gg.append(xshift)
    gg.sort()
    monomials = []
    for polynomial in gg:
      for monomial in polynomial.monomials():
        if monomial not in monomials:
          monomials.append(monomial)
    monomials.sort()
    for jj in range(1, tt + 1):
      for kk in range(floor(mm/tt) * jj, mm + 1):
        yshift = y^jj * polZ(u, x, y)^kk * modulus^(mm - kk)
        yshift = Q(yshift).lift()
        gg.append(yshift)
        monomials.append(u^kk * y^jj)
    nn = len(monomials)
    BB = Matrix(ZZ, nn)
    for ii in range(nn):
      BB[ii, 0] = gg[ii](0, 0, 0)
      for jj in range(1, ii + 1):
        if monomials[jj] in gg[ii].monomials():
          BB[ii, jj] = gg[ii].monomial_coefficient(monomials[jj]) * monomials[jj](UU,XX,YY)
    BB = remove_unhelpful(BB, monomials, modulus^mm, nn-1)
    nn = BB.dimensions()[0]
    if nn == 0:
      print "failure"
      return 0,0
    BB = BB.LLL()
    PR.<w,z> = PolynomialRing(ZZ)
    pol1 = pol2 = 0
    for jj in range(nn):
      pol1 += monomials[jj](w*z+1,w,z) * BB[0, jj] / monomials[jj](UU,XX,YY)
      pol2 += monomials[jj](w*z+1,w,z) * BB[1, jj] / monomials[jj](UU,XX,YY)
    PR.<q> = PolynomialRing(ZZ)
    rr = pol1.resultant(pol2)
    if rr.is_zero() or rr.monomials() == [1]:
      print "the two first vectors are not independant"
      return 0, 0
    rr = rr(q, q)
    soly = rr.roots()
    if len(soly) == 0:
      print "Your prediction (delta) is too small"
      return 0, 0
    soly = soly[0][0]
    ss = pol1(q, soly)
    solx = ss.roots()[0][0]
    return solx, soly

def boneh_durfee(n, e):
  delta = RR(0.167) # d ~ n^0.167
  m = 5
  t = round((1-2*delta) * m)
  X = ZZ(2*floor(n^delta))
  # we have n = p^2q. so `phi(n) = n + {-(pq+pr+qr) + p+q+r)} - 1`.
  # we reconsidered boneh-durfee's attack then we have `x(A+y) + 1 = 0 mod e` where `A = (n-1)`
  # and (x, y) = (k, -(pq+pr+qr)+p+q+r). 
  Y = ZZ(floor(n^(2/3)))
  P.<x,y> = PolynomialRing(ZZ)
  A = ZZ((n-1)/2)
  pol = 1 + x * (A + y)
  solx, soly = boneh_durfee_small_roots(pol, e, m, t, X, Y)
  print solx, soly
  if solx > 0:
    return int(pol(solx, soly) / e)
  return 0

if __name__ == "__main__":
  N = 1696852658826990842058316561963467335977986730245296081842693913454799128341723605666024757923000936875008280288574503060506225324560725525210728761064310034604441130912702077320696660565727540525259413564999213382434231194132697630244074950529107794905761549606578049632101483460345878198682237227139704889943489709170676301481918176902970896183163611197618458670928730764124354693594769219086662173889094843054787693685403229558143793832013288487194871165461567
  e = 814161885590044357190593282132583612817366020133424034468187008267919006610450334193936389251944312061685926620628676079561886595567219325737685515818965422518820810326234612624290774570873983198113409686391355443155606621049101005048872030700143084978689888823664771959905075795440800042648923901406744546140059930315752131296763893979780940230041254506456283030727953969468933552050776243515721233426119581636614777596169466339421956338478341355508343072697451
  print boneh_durfee(N, e)
```

等一下，这题目在哪里，完全没有提到N和e是怎么来的，e怎么这么大啊？然后我去搜了下，草，这是解题脚本，真正的[wp](https://masterpessimistaa.wordpress.com/2017/11/24/asis-finals-ctf-2017-gracias-writeup/)在这。题目都没有怎么写题啊……更别说理解了。

- ### Flag
    > ASIS{Wiener_at7ack_iN_mUlt1_Prim3_RSA_iZ_f34sible_t0O!}
