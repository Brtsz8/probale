import math

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

#### PODPUNKT 3 #########################
class City:
    def __init__(self, id: int, name: str, population: int, lat: float, lon: float):
        self.id = id
        self.name = name
        self.population = population
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return self.name

    def distance(self, other):
        return ((self.lat - other.lat)**2 + (self.lon - other.lon)**2)**0.5


# ---------- WCZYTYWANIE ----------
def wczytaj_miasta(plik, n):
    miasta = []
    with open(plik, "r") as f:
        next(f)
        for line in f.readlines()[:n]:
            d = line.split()
            miasta.append(City(int(d[0]), d[1], int(d[2]), float(d[3]), float(d[4])))
    return miasta


# ---------- DŁUGOŚĆ CYKLU ----------
def dlugosc_trasy(trasa, miasta):
    suma = 0
    for i in range(len(trasa) - 1):
        suma += miasta[trasa[i]].distance(miasta[trasa[i+1]])
    suma += miasta[trasa[-1]].distance(miasta[trasa[0]])
    return suma


# ---------- PERMUTACJE ----------
def permutacje(arr, start, best, miasta):
    if start == len(arr):
        d = dlugosc_trasy(arr, miasta)
        if d < best[0]:
            best[0] = d
            best[1] = arr[:]
        return

    for i in range(start, len(arr)):
        arr[start], arr[i] = arr[i], arr[start]
        permutacje(arr, start + 1, best, miasta)
        arr[start], arr[i] = arr[i], arr[start]


# ---------- KOMBINACJE ----------
def kombinacje(n, m, start, aktualne, wynik):
    if len(aktualne) == m:
        wynik.append(aktualne[:])
        return

    for i in range(start, n):
        aktualne.append(i)
        kombinacje(n, m, i + 1, aktualne, wynik)
        aktualne.pop()


# ---------- MAIN ----------
def tsp_dla_podzbiorow(plik, n, m):
    miasta = wczytaj_miasta(plik, n)

    podzbiory = []
    kombinacje(n, m, 0, [], podzbiory)

    global_best = [float('inf'), None]

    for subset in podzbiory:
        perm = subset[:]  # kopia!

        best_local = [float('inf'), None]

        # KLUCZ: fixujemy pierwszy element
        permutacje(perm, 1, best_local, miasta)

        # zapis najlepszego
        if best_local[1] is not None and best_local[0] < global_best[0]:
            global_best[0] = best_local[0]
            global_best[1] = best_local[1][:]

    # wynik
    if global_best[1] is None:
        print("Nie znaleziono trasy!")
    else:
        najlepsza_trasa = [str(miasta[i]) for i in global_best[1]]
        print("Najlepsza trasa:", najlepsza_trasa)
        print("Długość:", global_best[0])


# ---------- URUCHOMIENIE ----------
tsp_dla_podzbiorow("MPI lab 1 - spain.txt", n=6, m=6)


#PODPUNKT 4######################3
import random

def suma_populacji_bez_powtorzen(miasta, kombinacja):
    return sum(miasta[i].population for i in set(kombinacja))


def prawdopodobienstwo(plik, n, m, proby=100000):
    miasta = wczytaj_miasta(plik, n)

    total_pop = sum(city.population for city in miasta)
    dol = 0.4 * total_pop
    gora = 0.6 * total_pop

    trafione = 0

    for _ in range(proby):
        # losowanie z powtórzeniami
        kombinacja = [random.randint(0, n-1) for _ in range(m)]

        # liczenie bez powtórzeń
        pop = suma_populacji_bez_powtorzen(miasta, kombinacja)

        if dol <= pop <= gora:
            trafione += 1

    return trafione / proby


# uruchomienie
p = prawdopodobienstwo("MPI lab 1 - spain.txt", n=6, m=4)
print("Prawdopodobieństwo:", p)