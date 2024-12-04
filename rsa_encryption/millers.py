# millers algorithm assignment
import random


def isPrime(p):
    for i in range(20):
        ok = MillersTest(p)
        if not ok:
            return False # definitely composite
    return True #probably prime



def MillersTest(p):
    T = p - 1
    s = 0
    while T % 2 == 0:
        T = T // 2
        s += 1
    b = random.randrange(2, p)
    if pow(b, T, p) == 1:
        return True
    for i in range(s):
        if pow(b,T,p) == p - 1:
            return True
        T *= 2
    return False
