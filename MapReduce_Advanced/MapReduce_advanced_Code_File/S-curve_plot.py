import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def probability(s, r, b):
    # s: similarity
    # r: rows (per band)
    # b: number of bands
    return 1 - (1 - s**r)**b

#1. r=3 and b=10:
results = pd.DataFrame({
    'Jaccard similarity (S)': [],
    'Probability of becominga candidate (P)': [],
    'r,b': []
})

for s in np.arange(0.01, 1, 0.01):
        b = 10
        r = 3
        P = probability(s, r, b)
        results = results.append({
            'Jaccard similarity (S)': s,
            'Probability of becominga candidate (P)': P,
            'r,b': f"{r},{b}"
        }, ignore_index=True)
# plot line graph
sns.set(rc={'figure.figsize':(10,5)})
ax = sns.lineplot(data=results, x='Jaccard similarity (S)', y='Probability of becominga candidate (P)', hue='r,b', color='#965786')
ax.set(title="S-curve")

#2. r=6 and b=20:
results = pd.DataFrame({
    'Jaccard similarity (S)': [],
    'Probability of becominga candidate (P)': [],
    'r,b': []
})

for s in np.arange(0.01, 1, 0.01):
        b = 20
        r = 6
        P = probability(s, r, b)
        results = results.append({
            'Jaccard similarity (S)': s,
            'Probability of becominga candidate (P)': P,
            'r,b': f"{r},{b}"
        }, ignore_index=True)
# plot line graph
sns.set(rc={'figure.figsize':(10,5)})
ax = sns.lineplot(data=results, x='Jaccard similarity (S)', y='Probability of becominga candidate (P)', hue='r,b', color='#965786')
ax.set(title="S-curve")


#3. r=5 and b=50:
results = pd.DataFrame({
    'Jaccard similarity (S)': [],
    'Probability of becominga candidate (P)': [],
    'r,b': []
})

for s in np.arange(0.01, 1, 0.01):
        b = 50
        r = 5
        P = probability(s, r, b)
        results = results.append({
            'Jaccard similarity (S)': s,
            'Probability of becominga candidate (P)': P,
            'r,b': f"{r},{b}"
        }, ignore_index=True)
# plot line graph
sns.set(rc={'figure.figsize':(10,5)})
ax = sns.lineplot(data=results, x='Jaccard similarity (S)', y='Probability of becominga candidate (P)', hue='r,b', color='#965786')
ax.set(title="S-curve")