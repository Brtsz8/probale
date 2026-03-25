import random
import math
from collections import Counter
from itertools import permutations


# =========================
# PODSTAWA 1
# Generator liniowy
# =========================
class LinearGenerator:
    def __init__(self, a: int, c: int, m: int, seed: int = 1):
        self.a = a
        self.c = c
        self.m = m
        self.seed = seed

    # generate next integer
    def __generate_number(self) -> int:
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed

    # return number in (0,1)
    def generate_probability(self) -> float:
        return self.__generate_number() / self.m

    def generate_probabilities(self, n: int):
        for _ in range(n):
            yield self.generate_probability()

    def generate_number(self, m: int = None) -> int:
        if m is None:
            m = self.m
        return int(m * self.generate_probability())


# =========================
# PODSTAWA 2
# Generator rejestrowy (LFSR)
# =========================
class RegisterGenerator:
    def __init__(self, p: int, q: int, seed: int = 2**31, accuracy: int = 31):
        self.p = p
        self.q = q
        self.size = p + q
        self.seed = seed
        self.accuracy = accuracy

    # generate single bit
    def __generate_bit(self) -> int:
        p_bit = (self.seed >> (self.p - 1)) & 1
        q_bit = (self.seed >> (self.q - 1)) & 1

        bit = p_bit ^ q_bit  # xor

        # shift register
        self.seed >>= 1
        self.seed |= bit << self.size

        return bit

    # build float number from bits
    def generate_probability(self) -> float:
        result = 0
        weight = 0.5

        for _ in range(self.accuracy):
            if self.__generate_bit() == 1:
                result += weight
            weight /= 2

        return result


# =========================
# WSPOLNE: buckety
# =========================
class Bucket:
    def __init__(self, min_val, max_val):
        self.min = min_val
        self.max = max_val
        self.count = 0


def split_into_buckets(data, bucket_count):
    buckets = [Bucket(i / bucket_count, (i + 1) / bucket_count) for i in range(bucket_count)]

    for x in data:
        index = min(int(x * bucket_count), bucket_count - 1)
        buckets[index].count += 1

    return buckets


# =========================
# TEST CHI-KWADRAT (brakowalo)
# =========================
def chi_square_test(buckets, n):
    expected = n / len(buckets)
    chi2 = 0

    for b in buckets:
        chi2 += (b.count - expected) ** 2 / expected

    return chi2


# =========================
# UZUPELNIENIE 1u
# Monte Carlo - K orlow pod rzad
# =========================
def monte_carlo_heads(N, I, K):
    success = 0

    for _ in range(N):
        seq = [random.choice(["H", "T"]) for _ in range(I)]

        # check if sequence contains K heads in row
        for i in range(I - K + 1):
            if all(x == "H" for x in seq[i:i+K]):
                success += 1
                break

    return success / N


# =========================
# UZUPELNIENIE 2u
# pole czesci wspolnej kol
# =========================
def monte_carlo_area(N, R):
    inside = 0

    for _ in range(N):
        x = random.random()
        y = random.random()

        # circle 1 (center 0.5,0.5 radius 1)
        c1 = (x - 0.5)**2 + (y - 0.5)**2 <= 1

        # circle 2 (center 0,0 radius R)
        c2 = x**2 + y**2 <= R**2

        if c1 and c2:
            inside += 1

    return inside / N


# =========================
# DODATKOWE 3
# Mississippi permutation
# =========================
def mississippi_probability():
    word = "mississippi"

    perms = set(permutations(word))
    good = 0

    for p in perms:
        ok = True
        for i in range(len(p)-1):
            if p[i] == p[i+1]:
                ok = False
                break
        if ok:
            good += 1

    return good / len(perms)

def mississippi_mc(trials=100000):
    base = Counter("mississippi")
    good = 0

    for _ in range(trials):
        counts = base.copy()
        word = []

        # build permutation step by step
        for _ in range(11):
            letters = list(counts.keys())
            weights = list(counts.values())

            choice = random.choices(letters, weights=weights)[0]
            word.append(choice)

            counts[choice] -= 1
            if counts[choice] == 0:
                del counts[choice]

        # check condition
        ok = True
        for i in range(len(word) - 1):
            if word[i] == word[i+1]:
                ok = False
                break

        if ok:
            good += 1

    return good / trials
# =========================
# MAIN TEST
# =========================
N = 10000
K = 10

lin = LinearGenerator(16807, 0, 2**31 - 1, seed=1)
reg = RegisterGenerator(7, 3, seed=15)

lin_data = [lin.generate_probability() for _ in range(N)]
reg_data = [reg.generate_probability() for _ in range(N)]

lin_buckets = split_into_buckets(lin_data, K)
reg_buckets = split_into_buckets(reg_data, K)

print("Chi2 linear:", chi_square_test(lin_buckets, N))
print("Chi2 register:", chi_square_test(reg_buckets, N))

print("Monte Carlo heads:", monte_carlo_heads(1000, 10, 3))
print("Area:", monte_carlo_area(100000, 0.5))
print("Mississippi:", mississippi_mc(1000000))  # heavy!