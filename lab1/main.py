##############  PODPUNKT 1 #################
def iloscPorzodkow(n,m):
    silnia = 1
    while n > m:
        silnia *= n
        n -= 1
    return silnia

def wariacje(miasta, m, aktualne, used, licznik):
    if len(aktualne) == m:
        licznik[0] += 1
        print(f"{licznik[0]}: {tuple(aktualne)}")
        return

    for i in range(len(miasta)):
        if not used[i]:
            used[i] = True
            aktualne.append(miasta[i])
            wariacje(miasta, m, aktualne, used, licznik)
            aktualne.pop()
            used[i] = False


def wszystkie_wariacje(N, m):
    miasta = list(range(1, N + 1))
    used = [False] * N
    licznik = [0]
    wariacje(miasta, m, [], used, licznik)


# przykład
n = 5
m = 3
print("ilosc porzodkow: ", iloscPorzodkow(n,n-m))
wszystkie_wariacje(n, m)

####### PODPUNKT 2 ###################
def main():
    print("Liczba podzbiorów (z powtórzeniami):", ilosc_komb_powt(n, k))
    kombinacje_powt(0, 1)


def ilosc_komb_powt(n, k):
    # (n+k-1 choose k)
    wynik = 1
    for i in range(1, k + 1):
        wynik = wynik * (n + i - 1) // i
    return wynik


n = 5
k = 3

komb = [0] * k
count = 0


def kombinacje_powt(pozycja, start):
    global count
    if pozycja == k:
        count += 1
        print(count, tuple(komb))
        return

    for i in range(start, n + 1):
        komb[pozycja] = i
        kombinacje_powt(pozycja + 1, i)  #powtórzenia dozwolone

if __name__ == '__main__':
    main()