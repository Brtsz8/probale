def main():
    print("ilosc porzadkow dla n = ",n ,"m= ",m ,"to: ",iloscPorzadkow(n,n-m))
    porzadek(0)

def iloscPorzadkow(n, m):
    silnia_ret = 1
    while n > m:
        silnia_ret *= n
        n -= 1
    return silnia_ret

m = 4
n = 5
permutacja = [0] * m
used = [False] * (n+1)
count = 0

def porzadek(pozycja):
    global count
    if pozycja == m:
        count += 1
        print(count,permutacja)
        return
    for i in range(1, n+1):
        if not used[i]:
            permutacja[pozycja] = i
            used[i] = True
            porzadek(pozycja+1)
            used[i]=False
    return

if __name__ == '__main__':
    main()