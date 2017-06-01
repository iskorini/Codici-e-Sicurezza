import numpy as np

random_character_distribution = dict.fromkeys(list(map(chr, range(97, 123))), 1 / 26)
english_character_distribution = {'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253, 'e': 0.12702, 'f': 0.02228,
                                  'g': 0.02015, 'h': 0.06094, 'i': 0.06966, 'j': 0.00153, 'k': 0.00772, 'l': 0.04025,
                                  'm': 0.02406, 'n': 0.06749, 'o': 0.07507, 'p': 0.01929, 'q': 0.00095, 'r': 0.05987,
                                  's': 0.06327, 't': 0.09056, 'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150,
                                  'y': 0.01974, 'z': 0.00074}


def count_character(text):
    text_no_space = text.lower().replace(" ", "")
    occurences = dict()
    for character in list(map(chr, range(97, 123))):
        occurences[character] = text_no_space.count(character)
    for character in occurences:
        occurences[character] /= sum(occurences.values())
    return occurences


def kullback_leibler_divergence(freq1, freq2):
    divergence = 0
    for letter in freq2:
        if letter not in freq1:
            return np.inf
        else:
            divergence += freq1[letter] * np.log2((freq1[letter] / freq2[letter]))
    return divergence


def shift(seq, n):
    return seq[n:] + seq[:n]


def hypotesis_testing(text):
    occurrences = count_character(text)
    english_result = []
    english_result_qp = []
    random_result_qp = []
    random_result = []
    for n in range(0, 26):
        shifted_occurences = dict(zip(list(occurrences.keys()), shift(list(occurrences.values()), n)))
        english_result.append(abs(kullback_leibler_divergence(english_character_distribution, shifted_occurences)))
        english_result_qp.append(abs(kullback_leibler_divergence(shifted_occurences, english_character_distribution)))
        random_result.append(abs(kullback_leibler_divergence(random_character_distribution, shifted_occurences)))
        random_result_qp.append(abs(kullback_leibler_divergence(shifted_occurences, random_character_distribution)))
    result = [] * 4  # result, divergence, an, bn
    if min(english_result) < min(random_result):
        result.append("H0")
        result.append(min(english_result))
        result.append(pow(2, (-26 * min(english_result_qp))))
    else:
        result.append("H1")
        result.append(min(random_result))
        result.append(pow(2, (-26 * min(random_result_qp))))
    result.append(pow(2, (-26 * result[1])))
    return result


if __name__ == '__main__':
    print(hypotesis_testing(open("Text/engltext1.txt").read()))
