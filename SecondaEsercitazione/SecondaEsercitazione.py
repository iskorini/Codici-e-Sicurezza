import math
import random
import timeit

color = ['\033[0m', '\033[31m', '\033[32m', '\033[33m', '\033[34m', '\033[35m', '\033[36m', '\033[37m',
         '\033[38m', '\033[39m', '\033[40m']


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
        m = m // 2
        r = r + 1
    xr.append(fast_exp_alg(x, m, n))
    for i in range(1, r + 1):
        xr.append(fast_exp_alg(xr[i - 1], 2, n))
    return (xr[0] != 1) and all(xi % n != n - 1 for xi in xr[0:-1])


def generate_random_prime(limit, accuracy):
    random_number = 0
    condition = True
    while condition:
        random_number = random.randint(1, limit)
        if random_number % 2 != 0:
            test_sample = [random.randint(2, limit) for i in range(0, accuracy)]
            condition = any(rabin_test(x, random_number) for x in test_sample)
    return random_number


def rsa_encrypt(m, kp):
    return fast_exp_alg(m, kp[0], kp[1])


def rsa_decrypt(c, km):
    return fast_exp_alg(c, km[0], km[1])


def generate_rsa_key(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    d = 7  # generare casualmente relativamente primo con phi
    e = extended_euclidean_algorithm(d, phi)
    kp = (e[1], n)
    km = (d, n)
    return kp, km


def generate_rsa_crt_key(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    d = 7  # generare casualmente relativamente primo con phi
    e = extended_euclidean_algorithm(d, phi)
    dp = d % (p - 1)
    if dp < 0:
        dp = dp + p - 1
    dq = d % (q - 1)
    if dq < 0:
        dq = dq + q - 1
    q_inv = extended_euclidean_algorithm(q, p)[1]
    kp = (e[1], n)
    km = (p, q, dp, dq, q_inv)
    return kp, km


def rsa_decrypt_crt(c, km):
    m1 = fast_exp_alg(c, km[2], km[0])
    m2 = fast_exp_alg(c, km[3], km[1])
    h = km[4] * (m1 - m2) % km[0]
    return m2 + h * km[1]


def decryptionexp(n, d, e):
    return None


def wrapper_prime():
    generate_random_prime(10 ** 100, 16)

if __name__ == '__main__':
    # print(extended_euclidean_algorithm(17, 60))
    # print(rabin_test(2, 457))
    # print(fast_exp_alg(3, 11, 10))
    # print([generate_random_prime(10**100, 4) for i in range(0, 1)])
    # print(rabin_test(2, 3))
    # public_key, private_key = generate_rsa_key(3, 11)
    # print(rsa_encrypt(8, public_key))
    # print(rsa_decrypt(rsa_encrypt(8, public_key), private_key))
    # public_key, private_key = generate_rsa_crt_key(3, 11)
    # encr = rsa_encrypt(8, public_key)
    # print(encr)
    # print(rsa_decrypt_crt(encr, private_key))
    print(timeit.timeit(wrapper_prime, number=1))
