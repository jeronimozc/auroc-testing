from lib import *
import numpy as np
import time
import csv
import sys

##############
# PARAMETERS #
##############

N = 15 # elementos en la muestra
p_min = 0.05 # minimo de probabilidad para ser significativo
shuffles = 1000 # numero de permutaciones
iterations = 1000 # numero de muestreos
fo = 1.0 # factor de fano
mu = 20 # media inicial de las distribuciones a comparar
delta = np.concatenate((np.linspace(0.0,1.0,7),
                        np.linspace(1.0,6.0,7),
                        np.linspace(8.0,10.0,3))) # diferencias de medias a probar

hyper_params = [iterations,shuffles,p_min,N,mu,fo]

##############
# SIMULATION #
##############

Q = np.empty_like(delta)
true_auroc = np.empty_like(delta)
start_time = time.time()
n_delta = delta.shape[0]
for r in xrange(n_delta):
    d = delta[r]
    g1 = [mu  ,np.sqrt(fo*mu    )]
    g2 = [mu+d,np.sqrt(fo*(mu+d))]
    true_auroc[r] = gauss_AUROC(g1,g2)
    q = 0.0  
    for i in xrange(iterations):
        if i==300 and q >= 3*97.0:
            q = q/i*iterations
            break
        sys.stdout.write(" : delta={}  {}/{}\t{}/{}     \r".format(d,r+1,n_delta,i+1,iterations))
        sys.stdout.flush()      
        sample1 = np.random.normal(loc=g1[0],scale=g1[1],size=(N,))
        sample2 = np.random.normal(loc=g2[0],scale=g2[1],size=(N,))    
        all_samples = np.concatenate((sample1,sample2))
        bins = make_bins(all_samples)
        distribution1 = np.histogram(sample1,bins=bins[0],density=True)[0]
        distribution2 = np.histogram(sample2,bins=bins[0],density=True)[0]
        roc = ROC(bins[1],distribution1,distribution2)
        auroc = AUROC(roc)
        p = 0.0        
        for s in xrange(shuffles):
            fake_auroc = shuffle_auroc(all_samples,bins,N)
            if fake_auroc>=auroc:
                p += 1.0
        p = p/shuffles
        if p<=p_min:
            q += 1.0
    Q[r] = q/iterations
time_elapsed = time.time()-start_time
sys.stdout.write("\n")    
    
#############
# DATA SAVE #
#############

print time_elapsed
with open("data_{}.csv".format(1), 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(hyper_params)
    writer.writerow(delta)
    writer.writerow(true_auroc)
    writer.writerow(Q)
