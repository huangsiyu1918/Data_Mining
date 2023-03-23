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

def freq_itemset_finder(freq_itemset, transaction_set, min_support):
    item_set=[] 
    
    item_set = pair_items(freq_itemset)
    item_set= list(set(item_set))
    new_freq_itemset = []
    for item in item_set:
        j=0
        for outer in transaction_set:
            if(set(item).issubset(outer)):
                j=j+1
        if(j>min_support): 
            new_freq_itemset.append([item,j]) 
            
    return(new_freq_itemset)


def Apriori_algo(min_support, transaction_list ):
    result_count = dict(Counter(i for sub in transaction_list for i in set(sub)))
    frequent_1_itemset = [key for key, value in result_count.items() if value >=min_support]
    freq_itemset = frequent_1_itemset
    
    freq_itemset = freq_itemset_finder(freq_itemset=freq_itemset, transaction_set=transaction_list, min_support=min_support)
    return(freq_itemset)


def randomized_algo(perct, min_support, transaction_list):
    num_sample = round(len(transaction_list) * perct/100)
    sample_set  = random.sample(transaction_list,num_sample)
    freq_itemset = Apriori_algo(min_support , sample_set)
    
    return(freq_itemset,sample_set )


# Reading the data set
with open('chess.dat') as f:
    basket = f
    transaction_list = []
    for row in basket:
        transaction_list.append(row.strip().split())


# min support threshold = 1 %
print("SIMPLE RANDOMIZED ALGOTIRHM min support threshold = 6000 and sample size = 1% ")
print("----------------------------------------------")
import time
start = time.process_time()

freq_dic_randomized_10, ran_sample = randomized_algo(perct= 1, min_support  =3000/100,  transaction_list= transaction_list)

end = time.process_time()  
print("Total time taken: ",end - start," sec")
print("Number of frequent item set (pairs): ",len(freq_dic_randomized_10))
print("Sample Size:", len(ran_sample))
print(freq_dic_randomized_10)