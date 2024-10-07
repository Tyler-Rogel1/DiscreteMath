import permutationGenerator

def main():
    n = int(input("enter an interger from 2 to 10: "))
    all_perms = permutationGenerator.return_all_perms(n)
    num_perms = len(all_perms)
    # print(all_perms)
    wins = 0
    for perm in all_perms:
        valid = True
        for i in perm:
            if perm.index(i) == i:
                valid = False
        if valid:
            wins += 1
                
        
    print(f"out of {num_perms} permutations, {wins} were won")
    print(f"the probability of winning is {wins/num_perms}")

if __name__ == '__main__':
    main()