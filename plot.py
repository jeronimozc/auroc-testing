import matplotlib.pyplot as plt
import numpy as np
import csv

with open('data_1.csv', 'rb') as csvfile:
    reader = csvfile.readlines()
    hyper_params = np.array(reader[0].split(" "),dtype=np.float64)
    delta = np.array(reader[1].split(" "),dtype=np.float64)
    true_auroc = np.array(reader[2].split(" "),dtype=np.float64)        
    Q = np.array(reader[3].split(" "),dtype=np.float64)

p_min  = hyper_params[2]
pr_str = ["$Iterations={:.0f}$","$Shuffles={:.0f}$","$p={}$","$N={:.0f}$","$\mu ={}$","$fano={}$"]
box_text = "\n".join(pr_str).format(*hyper_params)

fig = plt.figure(figsize=(17,7))

ax = fig.add_subplot(121)
ax.set_xlim(0.50,1.0),ax.set_ylim(0.0,1.1),ax.grid(True);
ax.set_xlabel("$AUROC$",fontsize=16),ax.set_ylabel("$q$",fontsize=20,rotation=0,labelpad=20);
ax.plot(true_auroc,Q,"-o")
ax.hlines(p_min,*ax.get_xlim(),lw=2.0,linestyle="--")

ax = fig.add_subplot(122)
ax.set_xlim(0.0,20.0),ax.set_ylim(0.0,1.1),ax.grid(True);
ax.set_xlabel("$delta$",fontsize=16);
plt.plot(delta,Q,"-o")

# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=1.0)
# place a text box in upper left in axes coords
ax.text(0.60, 0.36, box_text, transform=ax.transAxes, fontsize=14,
        verticalalignment='top', bbox=props)

plt.savefig("graph.pdf")
