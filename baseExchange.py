def fromBaseTen(alphabet, num):
    num = int(num)
    base = len(alphabet)
    result = ""
    quotient = num // base
    remainder = num % base
    num = quotient
    result = alphabet[remainder] + result
    while quotient != 0:
        quotient = num // base
        remainder = num % base
        num = quotient
        result = alphabet[remainder] + result
    return result

def toBaseTen(alphabet, num):
    num = str(num)
    base = len(alphabet)
    result = 0
    for i in range(len(num)):
        result += alphabet.index(num[i]) * base ** (len(num) - 1 - i)
    return result

print(toBaseTen("01", fromBaseTen("01", 241)))
print(fromBaseTen("01", 241))
print(fromBaseTen("01", toBaseTen("01", 241)))