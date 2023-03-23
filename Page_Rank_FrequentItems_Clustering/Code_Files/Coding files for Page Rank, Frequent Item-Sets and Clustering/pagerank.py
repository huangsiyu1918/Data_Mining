from collections import defaultdict
import operator
import itertools

edge_list = []
edges = defaultdict(list)
pr = {}


OutPutFilename = r'C:\Users\huang\Desktop\PageRank MBD\PageRank_Result.txt'

with open ("test2.txt", 'r') as e_file:
    edge_list = e_file.readlines()

#edge_list = edge_list[:10]

for edge in edge_list:
    from_, to_ = edge.split(',')
    from_, to_ = int(from_), int(to_)
    #print("from", from_)
    #print("to_", to_)

    if to_ not in edges[from_]:
        edges[from_].append(to_)
    if to_ not in pr:
        pr[to_] = 0
    if from_ not in pr:
        pr[from_] = 0

n = len(pr)
print("edges: ", edges)
#print(n)
pr = dict.fromkeys(pr,1/n)
nodes = defaultdict(list)
#print("from: ", edges)
#print("to: ", des)

for parent in edges:
    for child in edges[parent]:
        nodes[child].append([parent, len(edges[parent])])

for node in pr:
    if node not in nodes:
        nodes[node].append([])

nodes = dict(sorted(nodes.items()))
print(nodes)

def one_iter(nodes, d=0.15):

    for node in nodes:
        parents = nodes[node]
        update_pagerank(node, parents,d)
    # print()
    #normalize_pagerank(pr)
            
def PageRank(nodes, d, iteration=2):
    for i in range(iteration):
        one_iter(nodes, d)

def update_pagerank(node, parents, d):
        #print(f'parent: for {node} is: {[parent[0] for parent in parents]}, their pr: {[pr[parent[0]] for parent in parents]}')
        #print(f'outlink: for {[parent[0] for parent in parents]} is: {[parent[1] for parent in parents]}')
        pagerank_sum = 0
        for parent in parents:
            if len(parent) == 0:
                pagerank_sum += 0
            else:
                r = pr[parent[0]]
                outlinks = parent[1]
                pagerank_sum +=(r / outlinks)
                #sprint(pagerank_sum)

        #random_jumping = Decimal(d) / Decimal(n)
        #pr[node] = random_jumping + (Decimal(1) - Decimal(d)) * pagerank_sum
        pr[node] = (1-d)/(n) + d*pagerank_sum


PageRank(nodes, d=0.15)

pr_all = dict( sorted(pr.items(), key=operator.itemgetter(1),reverse=True))

with open(OutPutFilename, 'w') as f:
    for value in pr_all:
        f.write('{:<12}  {:>12} \n'.format(value, pr_all[value]))
    f.close()