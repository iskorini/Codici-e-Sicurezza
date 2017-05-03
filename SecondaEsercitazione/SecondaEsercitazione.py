import math
import random


def fast_exp_alg(a, n, m):
    d, c = 1, 0
    bin_n = "{0:b}".format(n)
    for i in bin_n:
        d = (d * d) % m
        if int(i) == 1:
            d = (d * a) % m
    return d


def extended_euclidean_algorithm(a, b):
    rm = b
    rm1 = a
    qm1 = 1
    t = 0
    while rm1 != 0:
        q = math.floor(rm / rm1)
        temp = t
        t = qm1
        qm1 = temp - q * qm1
        temp = rm
        rm = rm1
        rm1 = temp - q * rm1
    if t < 0:
        t = t + b
    return rm, t


def rabin_test(x, n):
    m, r, xr = n - 1, 0, []
    while m % 2 == 0:
        m = int(m / 2)
        r = r + 1
    xr.append(fast_exp_alg(x, m, n))
    for i in range(1, r + 1):
        xr.append(fast_exp_alg(xr[i - 1], 2, n))
    return (xr[0] != 1) & all(xi % n != n - 1 for xi in xr[0:-1])


def generate_random_prime(limit):
    random_number = random.randint(1, limit)
    while random_number % 2 == 0:
        random_number = random.randint(1, limit)
    n_baton = int(math.floor(random_number / 4)) * 3
    while any(rabin_test(i, random_number) is True for i in range(2, n_baton)):
        random_number = random.randint(1, limit)
        while random_number % 2 == 0:
            random_number = random.randint(1, limit)
        print(random_number)
        n_baton = math.floor(random_number / 4) * 3
    return random_number


if __name__ == '__main__':
    # print(extended_euclidean_algorithm(17, 60))
    # print(rabin_test(2, 457))
    # print(fast_exp_alg(3, 11, 10))
    print(generate_random_prime(500))
