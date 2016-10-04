using Distributions
#using lib

function gauss_AUROC(g1,g2)
    """
    Require dos argumentos, cada uno una tupla que contenga las caracetristicas de una gaussiana:
    la primera entrada de la tupla debe ser el promedio y la segunda la desviacion estandar.
    Ref: Carnevale et al, 2013
    """
    D = abs(g2[0]-g1[0])/np.sqrt(0.5*(g1[1]+g2[1]))
    return 0.5*erfc(-0.5*D)
end

##############
# PARAMETERS #
##############

N = 20 # elementos en la muestra
p_min = 0.05 # minimo de probabilidad para ser significativo
shuffles = 1000 # numero de permutaciones
iterations = 1000 # numero de muestreos
fo = 1.0 # factor de fano
mu = 20 # media inicial de las distribuciones a comparar
delta = 0
#np.concatenate((np.linspace(0.0,3.0,7),np.linspace(3.0,15.0,5))) # diferencias de medias a probar
hyper_params = [iterations,shuffles,p_min,N,mu,fo]
dist1 = Normal(mu, sqrt(fo*mu))
dist1 = Normal(mu+delta, sqrt(fo*(mu+delta)))

sample1 = rand(dist1, N)
sample2 = rand(dist2, N)

writecsv("simulation.csv", cat(2,hyper_params,sample1,sample2))
