import random



def generate_uniform_transformed(n=100000):
    values = []
    for _ in range(n):
        u = random.random()
        y = 100 * u + 50
        values.append(y)
    return values


def count_intervals(values):
    bins = [0] * 10
    for v in values:
        index = int((v - 50) // 10)
        if index == 10:
            index = 9
        bins[index] += 1
    return bins


def print_intervals(bins):
    for i in range(10):
        start = 50 + i * 10
        end = start + 10
        print(f"({start}, {end}): {bins[i]}")


def discrete_distribution(n=100000):
    count = [0, 0, 0, 0]

    for _ in range(n):
        u = random.random()

        if u < 0.1:
            x = 1
        elif u < 0.3:
            x = 2
        elif u < 0.6:
            x = 3
        else:
            x = 4

        count[x - 1] += 1

    return count


def main():
    print("=== Zadanie 1: Rozkład jednostajny U(50,150) ===")
    values = generate_uniform_transformed()
    bins = count_intervals(values)
    print_intervals(bins)


    #plot_histogram(values)

    print("\n=== Zadanie 2: Rozkład dyskretny ===")
    counts = discrete_distribution()
    for i in range(4):
        print(f"{i+1}: {counts[i]}")


if __name__ == "__main__":
    main()
