import random


# ==========================================================
# ZADANIE 1 — ROZKŁAD JEDNOSTAJNY U(a,b)
# Metoda odwróconej dystrybuanty:
# Y = a + (b-a)U
# gdzie U ~ U(0,1)
# ==========================================================

def generate_uniform_transformed(a, b, n):
    """
    Generuje n liczb o rozkładzie jednostajnym U(a,b)

    Wzór matematyczny:
    Y = a + (b-a)*U

    gdzie:
    U ~ U(0,1) — liczba losowa od 0 do 1
    a — początek przedziału
    b — koniec przedziału
    """

    values = []

    for _ in range(n):
        # losujemy liczbę z przedziału (0,1)
        u = random.random()

        # przekształcenie odwrotnej dystrybuanty
        y = a + (b - a) * u

        values.append(y)

    return values


def count_intervals(values, a, b, num_bins):
    """
    Dzieli przedział <a,b> na num_bins części
    i liczy ile wartości wpada do każdego przedziału

    To odpowiada budowie histogramu.
    """

    bins = [0] * num_bins

    # szerokość pojedynczego przedziału
    bin_width = (b - a) / num_bins

    for v in values:

        # wyznaczenie indeksu przedziału
        index = int((v - a) // bin_width)

        # zabezpieczenie dla wartości = b
        if index == num_bins:
            index = num_bins - 1

        bins[index] += 1

    return bins


def print_intervals(bins, a, b):
    """
    Wypisuje liczności w przedziałach
    """

    num_bins = len(bins)
    bin_width = (b - a) / num_bins

    for i in range(num_bins):

        start = a + i * bin_width
        end = start + bin_width

        print(f"({start:.2f}, {end:.2f}): {bins[i]}")


# ==========================================================
# ZADANIE 2 — ROZKŁAD DYSKRETNY
# Metoda odwróconej dystrybuanty dla rozkładu dyskretnego
#
# Wzór z PDF:
# X = min { k : U ≤ suma(p_i) }
#
# Czyli:
# dodajemy prawdopodobieństwa aż suma przekroczy U
# ==========================================================

def discrete_distribution(probabilities, n):
    """
    Generuje rozkład dyskretny
    probabilities — lista prawdopodobieństw [p1,p2,p3,...]

    Warunek:
    suma(probabilities) = 1
    """

    k = len(probabilities)

    # liczniki wyników
    counts = [0] * k

    # tworzymy dystrybuantę (sumy częściowe)
    cumulative = []

    total = 0

    for p in probabilities:
        total += p
        cumulative.append(total)

    # generowanie liczb
    for _ in range(n):

        # losujemy U ~ U(0,1)
        u = random.random()

        # szukamy pierwszego progu ≥ u
        for i in range(k):

            if u < cumulative[i]:

                counts[i] += 1
                break

    return counts

# FUNKCJA GŁÓWNA

def main():

    # ------------------------------------------
    # PARAMETRY — można dowolnie zmieniać
    # ------------------------------------------

    n = 100000     # liczba losowań

    # Rozkład jednostajny
    a = 50         # początek przedziału
    b = 150        # koniec przedziału
    num_bins = 10  # liczba podprzedziałów

    # Rozkład dyskretny
    probabilities = [0.1, 0.2, 0.3, 0.4]

    # ------------------------------------------
    # ZADANIE 1
    # ------------------------------------------

    print("=== Zadanie 1: Rozkład jednostajny ===")
    print(f"U({a},{b})")
    print()

    values = generate_uniform_transformed(a, b, n)

    bins = count_intervals(values, a, b, num_bins)

    print_intervals(bins, a, b)

    # ------------------------------------------
    # ZADANIE 2
    # ------------------------------------------

    print("\n=== Zadanie 2: Rozkład dyskretny ===")
    print(f"Prawdopodobieństwa: {probabilities}")
    print()

    counts = discrete_distribution(probabilities, n)

    for i in range(len(counts)):
        print(f"{i+1}: {counts[i]}")


# ==========================================================

if __name__ == "__main__":
    main()