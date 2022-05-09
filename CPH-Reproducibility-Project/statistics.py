import json
import csv
import math
from time import time
from scipy.stats import pearsonr
import numpy

print(time())
data = []
data2 = []
path = []
path.append('./data/Chronic_Diseases_Prevalence_Dataset.csv')


for p in path:
    with open(p, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            data.append(row)

#print(data[0])
k='./data/ward_latlong.csv'
with open(k, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for row in reader:
        data2.append(row)

table={}
for d in data:
    code = d["Ward Code"]
    diabetes = float(d["Diabetes Mellitus (Diabetes) Prevalence_2009"])
    obesity =  float(d["Obesity Prevalence_2008"])
    hyper = float(d["Hypertension Prevalence_2008"])
    #print(diabetes)
    table[code] = {
        "diabetes": diabetes,
        "obesity": obesity,
        "hyper": hyper,
    }

for dd in data2:
    code = dd["wdcd"]
    longi = float(dd["longitude"])
    lati = float(dd["latitude"])
    if code not in table:
        continue
    table[code]["lo"] = longi
    table[code]["la"] = lati

#print(table)

pairs = []
for a in table:
    for b in table:
        if (a==b):
            continue
        lo_a = table[a]["lo"]
        la_a = table[a]["la"]
        lo_b = table[b]["lo"]
        la_b = table[b]["la"]
        distance = (lo_a-lo_b) * (lo_a-lo_b) + (la_a-la_b) * (la_a-la_b) 
        distance = math.sqrt(distance) * 100

        diabetes_a = table[a]["diabetes"]
        diabetes_b = table[b]["diabetes"]
        obesity_a = table[a]["obesity"]
        obesity_b = table[b]["obesity"]
        hyper_a = table[a]["hyper"]
        hyper_b = table[b]["hyper"]
        data1= [diabetes_a, obesity_a,hyper_a]
        data2= [diabetes_b, obesity_b,hyper_b]
        if (max([diabetes_a,diabetes_b]) < 1e-5) or (abs(diabetes_b-diabetes_a) < 1e-5):
            continue
        # calculate covariance matrix
        corr, _ = pearsonr(data1, data2)
        
        if (numpy.isnan(corr)):
            continue
        #print(corr)
        difference = abs(obesity_b-obesity_a)/abs(diabetes_b-diabetes_a)
        diff = difference
        pairs.append([distance,1-corr])


pairs=sorted(pairs)
count = {}
value = {}
print(pairs[0])
for p in pairs:
    x = p[0]
    y=p[1]
    group = int(x)
    if group not in count:
        count[group] = 0
        value[group] = 0
    count[group] +=1
    value[group] += y

#print(count, value)
k='./result/correlation-distance.csv'
with open(k, 'w', newline='') as csvfile:
    fieldnames = ['distance', 'diff']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for g in count:
        avg = value[g]/count[g]
        #print(avg)
        writer.writerow({'distance': g, 'diff': avg})


k="./result/correlation-distance2.csv"
with open(k, 'w', newline='') as csvfile:
    fieldnames = ['distance', 'diff']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()

    for g in pairs:
        
        #print(avg)
        writer.writerow({'distance': g[0], 'diff': g[1]})

print(time())