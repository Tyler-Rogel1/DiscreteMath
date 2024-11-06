import random

def is_prime(n, k=10):
    # Handle small numbers and base cases
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    

    # Write n-1 as 2^s * e with e odd
    s = 0
    e = n - 1
    # take out as many 2s as possible
    while e % 2 == 0:
        e //= 2
        s += 1
    

    # Test k times
    for _ in range(k):
        # pick random base
        b = random.randint(2, n - 2)
        remainder = pow(b, e, n)
        
        if remainder == 1 or remainder == n - 1:
            continue
        
        for _ in range(s - 1):
            remainder = pow(remainder, 2, n)
            if remainder == n - 1:
                break
        else:
            return False  # Composite
    return True  # Probably prime

def main():
    n = int(input("Enter a number: "))
    if is_prime(n):
        print(f"{n} is a prime number.")
    else:
        print(f"{n} is not a prime number.")
    print(is_prime(9154514856374024582543855878978670001446941608236501398571266349456394752049257780072447789718173383*1869620605091761782636386310554335036348292099414010576305059712928435185308391931391489858135705153))
    print(is_prime(17570848787052001934855724936897207706761100609709313965721206506741040400618096612083094691341080714132976606967146684118814703682124253988953297570918959316755806992007302776953349877844396691945201*1869620605091761782636386310554335036348292099414010576305059712928435185308391931391489858135705153))

if __name__ == "__main__":
    main()