function gauss_AUROC(g1,g2)
    """
    Require dos argumentos, cada uno una tupla que contenga las caracetristicas de una gaussiana:
    la primera entrada de la tupla debe ser el promedio y la segunda la desviacion estandar.
    Ref: Carnevale et al, 2013
    """
    D = abs(g2[0]-g1[0])/np.sqrt(0.5*(g1[1]+g2[1]))
    return 0.5*erfc(-0.5*D)
end

function make_bins(sample,percent=0.01):
    start,stop = sample.min(),sample.max()
    start,stop = floor(start),ceil(stop)
    bin_width = round((stop-start)*percent,3)
    bins = np.arange(start-2*bin_width,stop+2*bin_width,bin_width)
    return bins,bin_width
end

function integrate(bin_width,X,start=0):
    integral = np.sum(X[start:]*bin_width)
    return integral
end

function ROC(bin_width,X,Y):
    assert X.shape==Y.shape, "Non-matching shapes of the distributions!"
    n_bins = X.shape[0]
    roc = np.empty((n_bins,2))
    for i in xrange(n_bins):
        IX = integrate(bin_width,X,start=i)
        IY = integrate(bin_width,Y,start=i)
        roc[i] = IX,IY
    return roc
end

function AUROC(roc):
    x,y = roc[::-1,0],roc[::-1,1]
    widths = np.diff(x)
    heights = y[:-1]+np.diff(y)/2
    area = np.sum(heights*widths)
    if area<0.5:
        area = 1.0-area 
    return area
end

function gauss_AUROC(g1,g2):
    """
    Require dos argumentos, cada uno una tupla que contenga las caracetristicas de una gaussiana:
    la primera entrada de la tupla debe ser el promedio y la segunda la desviacion estandar.
    Ref: Carnevale et al, 2013
    """
    D = abs(g2[0]-g1[0])/np.sqrt(0.5*(g1[1]+g2[1]))
    return 0.5*erfc(-0.5*D)
end

function shuffle_auroc(all_samples,bins,N):
    indices = range(N)
    idx1 = np.random.choice(indices,size=(N,),replace=False)
    idx2 = np.array(list(set(indices).difference(set(idx1))),dtype=int)
    shuffle1,shuffle2 = all_samples[idx1], all_samples[idx2]
    dist1 = np.histogram(shuffle1,bins=bins[0],density=True)[0]
    dist2 = np.histogram(shuffle2,bins=bins[0],density=True)[0]
    roc = ROC(bins[1],dist1,dist2)
    auroc = AUROC(roc)
    return auroc    
end    
