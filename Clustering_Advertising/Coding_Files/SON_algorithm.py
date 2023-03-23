import numpy as np
from collections import Counter 
from itertools import chain, combinations
import random

def pair_items(freq_itemset):
    item_set = []
    freq_itemset_1 = freq_itemset[::-1]

    for i in range(len(freq_itemset)):
        for j in range(len(freq_itemset_1)-1):
            if freq_itemset[i] != freq_itemset_1[j]:
                item_set.append(tuple([freq_itemset[i], freq_itemset_1[j]]))
            else:
                break
    return item_set


def freq_itemset_finder(freq_itemset, transaction_set, min_support_perct):
    item_set=[] 
    
    item_set = pair_items(freq_itemset)
    item_set= list(set(item_set))
    new_freq_itemset = {}
    result = []
    for chunk in transaction_set:
        for item in item_set:
            j=0
            for outer in chunk:
                if(set(item).issubset(outer)): # if the item set is a subset of transction set
                    j=j+1
            if item in new_freq_itemset:
                new_freq_itemset[item] = new_freq_itemset[item]+j
            else:
                new_freq_itemset[item] = j

    for key, value in new_freq_itemset.items():
        if value >= min_support_perct:
            result.append([key,value])
                
    return(result)

    
def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def divide_baskets(transaction_list, num_in_baskets):
    new_transaction_list = list(chunks(transaction_list, num_in_baskets))
    num_chunks = (len(new_transaction_list))
    return new_transaction_list, num_chunks

def SON_algo(min_support_perct, new_transaction_list, num_chunks):
    frequent_1_itemset = []
    min_sup = (1/num_chunks * min_support_perct)
    for chunk in new_transaction_list:
        result_count = dict(Counter(i for sub in chunk for i in set(sub)))
        for key, value in result_count.items():
            if value >= min_sup and key not in frequent_1_itemset:
                frequent_1_itemset.append(key)

    freq_itemset = frequent_1_itemset
    # print(freq_itemset)
    freq_itemset = freq_itemset_finder(freq_itemset=freq_itemset, transaction_set=new_transaction_list, min_support_perct=min_support_perct)
    
    return(freq_itemset) 


# Reading the data set
with open('chess.dat') as f:
    basket = f
    transaction_list = []
    for row in basket:
        transaction_list.append(row.strip().split())


# min support threshold = 1 %
print("SON ALGORITHM")
print("----------------------------------------------")
import time
start = time.process_time()

new_transaction_list, num_baskets = divide_baskets(transaction_list, 1000)
freq_dic = SON_algo(min_support_perct = 3000, new_transaction_list = new_transaction_list , num_chunks = num_baskets)

end = time.process_time()  
print("Total time taken: ",end - start," sec")
print("Number of frequent item set(pairs): ",len(freq_dic))
print("dataset size:", len(transaction_list))
print(freq_dic)