import numpy as np
from fractions import gcd
import math
import itertools

KEY1 = np.matrix('7 8; 19 3')
KEY2 = np.matrix('1 0 2; 10 20 15;0 1 2')


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)


def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


def matrix_inverse_module_n(numpy_matrix, n):
    det = np.rint(np.linalg.det(numpy_matrix)) % 26
    inverse = np.matrix(numpy_matrix)
    for i in range(0, numpy_matrix.shape[0]):
        for j in range(0, numpy_matrix.shape[1]):
            deleted = np.delete(np.delete(numpy_matrix, j, 0), i, 1)
            det_inverse = np.rint(modinv(det, n))
            inverse[i, j] = np.rint((((-1) ** (i + j)) * np.linalg.det(deleted) * det_inverse) % n)
    return inverse


def text_to_vector(text, key_dimension):
    text_no_space = text.replace(" ", "")
    dimension_text = math.ceil(len(text_no_space) / key_dimension) * key_dimension
    list = [ord('x') - 97] * dimension_text
    for i in range(0, len(text_no_space)):
        list[i] = (ord(text_no_space[i]) - 97)
    vector = np.array(list)
    return vector


def vector_to_text(vector):
    list = []
    [[list.append(chr(element.item(i) + 97)) for i in range(0, element.shape[1])] for element in vector]
    return ''.join(list)


def hill_cipher(plain_text, key):
    key_len = len(key)
    vector_plain_text = text_to_vector(plain_text, key_len)
    sub_plain_text = np.split(vector_plain_text, np.rint(len(vector_plain_text) / key_len))
    cipher_text = []
    [cipher_text.append(np.dot(key, sub_array) % 26) for sub_array in sub_plain_text]
    return vector_to_text(cipher_text)


def hill_decipher(cipher_text, key):
    plain_text = []
    cipher_text_vector = text_to_vector(cipher_text, len(key))
    cipher_text_vector_np = np.split(cipher_text_vector, np.rint(len(cipher_text_vector) / len(key)))
    key_inverse = matrix_inverse_module_n(key, 26)
    [plain_text.append(np.dot(key_inverse, sub_array) % 26) for sub_array in cipher_text_vector_np]
    return vector_to_text(plain_text)


def get_key_kpa(plain_text, cipher_text, block_dimension):
    cipher_text_vector = text_to_vector(cipher_text, block_dimension)
    cipher_text_vector_np = np.split(cipher_text_vector, len(cipher_text_vector) / block_dimension)
    plain_text_vector = text_to_vector(plain_text, block_dimension)
    plain_text_vector_np = np.split(plain_text_vector, len(plain_text_vector) / block_dimension)
    combination = itertools.combinations(list(range(0, len(plain_text_vector_np))), block_dimension)
    for element in list(combination):
        C = np.array([cipher_text_vector_np[i] for i in element]).T
        P = np.array([plain_text_vector_np[i] for i in element]).T
        if (gcd(np.rint(np.linalg.det(P)) % 26, 26) == 1):
            return np.dot(C, matrix_inverse_module_n(P, 26)) % 26
    return 0


if __name__ == '__main__':
    plain_text = "mangio la pizza sono il solo sveglio in tutta la citta bevo un bicchiere per pensare meglio per rivivere lo stesso sbaglio"
    print(plain_text)
    KEY_USED = KEY2
    cipher_text = hill_cipher(plain_text, KEY_USED)
    print(cipher_text)
    plain_text = hill_decipher(cipher_text, KEY_USED)
    print(plain_text)
    print(get_key_kpa(plain_text, cipher_text, len(KEY_USED)))
