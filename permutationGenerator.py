
def find_first_lt(a):
    j = len(a)-2
    while j >= 0 and a[j] > a[j+1]:
        j-=1
    return j

def make_swap(a, j):
    k = len(a)-1
    while a[j] > a[k]:
        k -= 1
    a[j], a[k] = a[k], a[j]
    return a

def fix_tail(a, j):
    r = len(a) - 1
    s = j + 1
    while r > s:
        a[r], a[s] = a[s], a[r]
        r -= 1
        s += 1
    return a

def find_next_perm(a):
    j = find_first_lt(a)
    if j != -1:
        make_swap(a, j)
        fix_tail(a, j)
    return a

def print_all_perms(n):
    a = []
    for i in range(n):
        a.append(i)
    reverse = a[::-1]
    print(''.join(map(str, a)))
    while a != reverse:
        find_next_perm(a)
        print(''.join(map(str, a)))

def return_all_perms(n):
    a = []
    for i in range(n):
        a.append(i)
    reverse = a[::-1]
    all_perms = []
    all_perms.append(a)
    # print(''.join(map(str, a)))
    # print(all_perms)
    while a != reverse:
        # print("pre findnext: ", all_perms)
        copy = a.copy()
        a = find_next_perm(copy)
        # print("pre appednd: ", all_perms)
        all_perms.append(a)
        # print(''.join(map(str, a)))
        # print(all_perms)
    return all_perms
    

def main():
    n = int(input("enter an integer from 1 to 9: "))
    print_all_perms(n)

if __name__ == '__main__':
    main()