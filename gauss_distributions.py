from lib import *
import numpy as np
import time
import csv
import sys

##############
# PARAMETERS #
##############

p_min = 0.05 # minimo de probabilidad para ser significativo
samples = [5,10,20] # elementos en la muestra
shuffles = 1000 # numero de permutaciones
iterations = 1000 # numero de muestreos
fo = 1.0 # factor de fano
mu = 20 # media inicial de las distribuciones a comparar
delta = np.concatenate((np.linspace(0.0,1.0,10),
                        np.linspace(1.0,6.0,10),
                        np.linspace(8.0,10.0,5))) # diferencias de medias a probar



##############
# SIMULATION #
##############

Q = np.empty_like(delta)
true_auroc = np.empty_like(delta)
simt_auroc = {}
start_time = time.time()
n_delta = delta.shape[0]
data = {}
for N in samples:
    sys.stdout.write("\nN = {}\n".format(N))
    sys.stdout.flush() 
    for r in xrange(n_delta):
        d = delta[r]
        g1 = [mu  ,np.sqrt(fo*mu    )]
        g2 = [mu+d,np.sqrt(fo*(mu+d))]
        truth = gauss_AUROC(g1,g2)
        true_auroc[r] = truth
        simt_auroc[truth] = np.empty((iterations,))
        for i in xrange(iterations):
            if i%10 == 0:
                sys.stdout.write("  delta={:.2f}  {}/{}\t{}/{}     \r".format(d,r+1,n_delta,i+1,iterations))
                sys.stdout.flush()      
            sample1 = np.random.normal(loc=g1[0],scale=g1[1],size=(N,))
            sample2 = np.random.normal(loc=g2[0],scale=g2[1],size=(N,))
            assert len(sample1)==len(sample2)==N, "crap"
            if i == 0:
                print sample1
            all_samples = np.concatenate((sample1,sample2))
            bins = make_bins(all_samples)
            distribution1 = np.histogram(sample1,bins=bins[0],density=True)[0]
            distribution2 = np.histogram(sample2,bins=bins[0],density=True)[0]
            roc = ROC(bins[1],distribution1,distribution2)
            simt_auroc[truth][i] = AUROC(roc)
    data[N] = simt_auroc
        
time_elapsed = time.time()-start_time
sys.stdout.write("\n")    
    
#############
# DATA SAVE #
#############

print time_elapsed
with open("distributions_{}.csv".format(0), 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(delta)
    writer.writerow(true_auroc)
    for N in samples:
        hyper_params = [iterations,shuffles,p_min,N,mu,fo]
        writer.writerow(hyper_params)
        simt_auroc = data[N]
        for auroc in true_auroc:
            writer.writerow(simt_auroc[auroc])
            if auroc == true_auroc[-1]:
                print simt_auroc[auroc]
  

