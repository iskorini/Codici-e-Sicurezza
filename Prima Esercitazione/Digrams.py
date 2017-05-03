import threading
import time
import math
import numpy as np
import sys
import matplotlib.pyplot as plt
import collections
from collections import defaultdict
import operator
from functools import reduce

mutex = threading.Lock()


def thread_safe_digrams(text, n, result_set):
    global mutex
    text_el = list(map(str.lower, filter(str.isalpha, text)))
    digrams = threading.local()
    digrams.value = {}
    for i in range(0, len(text_el) - n + 1):
        digram = ''.join(text_el[i:i + n])
        if digram not in list(digrams.value.keys()):
            digrams.value[digram] = 0
        digrams.value[digram] += 1
    mutex.acquire()
    for key in digrams.value:
        if key not in list(result_set.keys()):
            result_set[key] = 0
        result_set[key] += digrams.value[key]
    mutex.release()
    return 0


def multi_threading_digrams(text, n, thread_number):
    single_unit = math.floor((len(text) / thread_number))
    thread_list = []
    result_set = {}
    [thread_list.append(threading.Thread(target=thread_safe_digrams,
                                         args=(text[i * single_unit:(i * single_unit) + single_unit], n, result_set)))
     for i in range(0, thread_number - 1)]
    thread_list.append(threading.Thread(target=thread_safe_digrams,
                                        args=(text[(thread_number - 1) * single_unit:len(text)], n, result_set)))
    [t.start() for t in thread_list]
    [t.join() for t in thread_list]
    return (result_set, sum(result_set.values()))


def histogram_from_dic(d, b, max_digrams):
    if b == 0:
        plt.bar(range(len(d)), d.values(), align='center')
        plt.xticks(range(len(d)), list(d.keys()))
        plt.show()
    elif b == 1:
        ordered_dictionary_val_sorted = sorted(d.items(), key=operator.itemgetter(1))
        ordered_dictionary_val = collections.OrderedDict(ordered_dictionary_val_sorted)
        ordered_dictionary_key = collections.OrderedDict(sorted(d.items()))
        plt.subplot(211)
        plt.title("Ordine alfabetico")
        plt.bar(range(len(ordered_dictionary_key)), ordered_dictionary_key.values(), align='center', width=1.0)
        plt.subplot(212)
        plt.title("Ordine per occorrenze\r\n" + str(list(ordered_dictionary_val_sorted)[-max_digrams:]))
        plt.bar(range(len(ordered_dictionary_val)), ordered_dictionary_val.values(), align='center', width=1.0)
        plt.show()


def coincidence_index_dic(d):
    n = sum(d.values())
    return reduce((lambda x, y: x + y), (map((lambda x: (d[x] * (d[x] - 1)) / (n * (n - 1))), d)))


def entropy_dic(d):
    n = sum(d.values())
    entropy = reduce((lambda x, y: x + y), (map((lambda x: d[x] / n * math.log(d[x] / n)), d)))
    return (-1) * (entropy) / math.log(len(d.keys()))


if __name__ == '__main__':
    text = open(str(sys.argv[2]), encoding="utf8").read()
    print("1) Istogramma della frequenza delle 26 lettere")
    print("2) Dato q>0 in input, distribuzione empirica dei q-grammi")
    print("3) Dato q>0, indice di coincidenza ed entropia delle distribuzioni dei q-grammi")
    input_var = int(input("Inserire un numero da 1 a 3:"))
    if input_var == 1:
        result = multi_threading_digrams(text, 1, int(sys.argv[1]))[0]
        histogram_from_dic(collections.OrderedDict(sorted(result.items())), 0, 0)
    elif input_var == 2:
        input_var = int(input("inserire q: "))
        max_digrams = int(input("inserire quanti q-grammi più comuni si vogliono stampare: "))
        result = multi_threading_digrams(text, input_var, int(sys.argv[1]))[0]
        histogram_from_dic(result, 1, max_digrams)
    elif input_var == 3:
        input_var = int(input("inserire q: "))
        result = multi_threading_digrams(text, input_var, int(sys.argv[1]))[0]
        print("Indice di coincidenza:" + str(coincidence_index_dic(result)))
        print("Entropia:" + str(entropy_dic(result)))
