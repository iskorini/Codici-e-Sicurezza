import math
import random
import timeit

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
    if rm>1:
        t = "ND"
    return rm, t

def rabin_test(x, n):
    m, r, xr = n - 1, 0, []
    while m % 2 == 0:
        m = m // 2
        r = r + 1
    xr.append(fast_exp_alg(x, m, n))
    for i in range(1, r + 1):
        xr.append(fast_exp_alg(xr[i - 1], 2, n))
    return (xr[0] != 1) and all(xi % n != n - 1 for xi in xr[0:-1])


def generate_random_prime(minimum, limit, accuracy):
    random_number = 0
    condition = True
    while condition:
        random_number = random.randint(minimum, limit)
        if random_number % 2 != 0:
            test_sample = [random.randint(2, limit) for i in range(0, accuracy)]
            condition = any(rabin_test(x, random_number) for x in test_sample)
    return random_number


def rsa_encrypt(m, kp):
    return fast_exp_alg(m, kp[0], kp[1])


def rsa_decrypt(c, km):
    return fast_exp_alg(c, km[0], km[1])


def generate_rsa_key(p, q, d):
    n = p * q
    phi = (p - 1) * (q - 1)
    if d == 0:
        d = generate_random_prime(2, n-1, 5)
        while extended_euclidean_algorithm(d, phi)[0] != 1:
            d = generate_random_prime(2, n-1, 16)
    e = extended_euclidean_algorithm(d, phi)
    kp = (e[1], n)
    km = (d, n)
    return kp, km


def generate_rsa_crt_key(p, q, d):
    n = p * q
    phi = (p - 1) * (q - 1)
    if d == 0:
        d = generate_random_prime(2, n - 1, 5)
        while d != 1 and extended_euclidean_algorithm(d, phi)[0] != 1:
            d = generate_random_prime(2, n-1, 5)
    q_inv = extended_euclidean_algorithm(q, p)[1]
    p_inv = extended_euclidean_algorithm(p, q)[1]
    e = extended_euclidean_algorithm(d, phi)
    kp = (e[1], n)
    km = (p, q, d, p_inv*p, q_inv*q)
    return kp, km


def rsa_decrypt_crt(c, km):
    mp = fast_exp_alg(c, km[2], km[0])
    mq = fast_exp_alg(c, km[2], km[1])
    return ((mp * km[4]) + (mq * km[3]))%(km[0]*km[1])

