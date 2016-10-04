import matplotlib.pyplot as plt
import numpy as np
from lib import *
import csv

distros = {}
with open('distributions_0.csv', 'rb') as csvfile:
    reader = csvfile.readlines()
    delta = np.array(reader[0].split(" "),dtype=np.float64)
    true_auroc = np.array(reader[1].split(" "),dtype=np.float64)
    simt_auroc = {}
    l = true_auroc.shape[0]
    n = 0
    for i in xrange(l):
        auroc = true_auroc[i]
        hyper_params = np.array(reader[n*(l+1)+2  ].split(" "),dtype=np.float64)    
        sample       = np.array(reader[n*(l+1)+3+i].split(" "),dtype=np.float64)
        simt_auroc[auroc] = sample
        distros[auroc] = np.histogram(sample,bins=100,density=True)

p_min  = hyper_params[2]
pr_str = ["$Iterations={:.0f}$","$Shuffles={:.0f}$","$p={}$","$N={:.0f}$","$\mu ={}$","$fano={}$"]
box_text = "\n".join(pr_str).format(*hyper_params)

fig = plt.figure(figsize=(17,7))

ax = fig.add_subplot(121)
ax.set_xlim(0.50,1.0),ax.grid(True);#ax.set_ylim(0.0,1.1),
ax.set_xlabel("$AUROC$",fontsize=16),ax.set_ylabel("$q$",fontsize=20,rotation=0,labelpad=20);
i = 0
au = true_auroc[i]  
bins,hist = distros[au][1][:-1],distros[au][0]
bin_width = bins[1]-bins[0]
ax.bar(bins,hist,width=bin_width)   
ax.vlines(au,*ax.get_ylim(),lw=2.0,linestyle="--")

ax = fig.add_subplot(122)
ax.set_xlim(0.50,1.0),ax.grid(True);#ax.set_ylim(0.0,1.1),
ax.set_xlabel("$AUROC$",fontsize=16),ax.set_ylabel("$q$",fontsize=20,rotation=0,labelpad=20);
i = -1
au = true_auroc[i]
bins,hist = distros[au][1][:-1],distros[au][0]
bin_width = bins[1]-bins[0]
ax.bar(bins,hist,width=bin_width)   
ax.vlines(au,*ax.get_ylim(),lw=2.0,linestyle="--")

# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=1.0)
# place a text box in upper left in axes coords
ax.text(0.05, 0.95, box_text, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

plt.savefig("graph_distributions.pdf")
