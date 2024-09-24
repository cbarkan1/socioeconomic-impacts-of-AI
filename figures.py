"""
Creates figures in the report "Can an increase in productivity 
cause a decrease in GDP?"

"""


import numpy as np
import matplotlib.pyplot as plt


def f(K,L,a1,a2):
	""" Production function (Eq. 4)
	"""
	K1 = np.minimum(L*(alpha*a1/a2)**(1/(1-alpha)), K*np.ones_like(L))
	return a1*K1**alpha*L**(1-alpha) + a2*(K-K1)

def w(L):
	""" Labor supply function
	"""
	return w0/np.cos(L/L_max)

def outcomes(a2):
	""" Computes econonomic outcomes.
	
		Returns:
			Labor employed (L_star)
			GDP (f_star)
			Profit (Pi_star)
			Capital allocated to old tech (K1_star)
	"""
	L_list = np.linspace(0,200,10000)
	f_list = f(K,L_list,a1,a2)
	Pi_list = f_list - w(L_list)*L_list
	max_index = np.nanargmax(Pi_list)
	L_star = L_list[max_index]
	f_star = f_list[max_index]
	Pi_star = Pi_list[max_index]
	K1_star = min([L_star*(alpha*a1/a2)**(1/(1-alpha)), K])
	return L_star, f_star, Pi_star, K1_star


# Model parameters:
alpha = 0.5
w0 = 10
a1 = 23
K = 100
L_max = 400

# Compute outcomes
a2s = np.linspace(0,25,500)
Ls = np.zeros_like(a2s)
fs = np.zeros_like(a2s)
Pis = np.zeros_like(a2s)
K1s = np.zeros_like(a2s)

for i, a2 in enumerate(a2s):
	Ls[i], fs[i], Pis[i], K1s[i] = outcomes(a2)



# Figure 1

linewidth=2
fig, (a,b) = plt.subplots(1,2,figsize=(10,3))
a.plot(a2s,K-K1s,color='#c1121f',linewidth=linewidth)
a.plot(a2s,K1s,color='#669bbc',linewidth=linewidth)
a.spines[['right', 'top']].set_visible(False)
a.set_xlim(0,25)
a.set_ylim(-0.6,101)

b.plot(a2s,100*Ls/np.max(Ls),color='#2a9d8f',linewidth=linewidth)
b.spines[['right', 'top']].set_visible(False)
b.set_xlim(0,25)
b.set_ylim(-0.6,101)

plt.subplots_adjust(wspace=0.4)
#plt.savefig('K1.svg',transparent=True)


# Figure 2

linewidth=2
fig, (a,b) = plt.subplots(1,2,figsize=(10,3))
a.plot(a2s,Pis,color='#2a9d8f',linewidth=linewidth)
a.spines[['right', 'top']].set_visible(False)
a.set_xlim(0,25)
a.set_ylim(0,2500)

b.plot(a2s,fs,color='#2a9d8f',linewidth=linewidth)
b.spines[['right', 'top']].set_visible(False)
b.set_xlim(0,25)
b.set_ylim(0,2500)

plt.subplots_adjust(wspace=0.4)
#plt.savefig('GDP.svg',transparent=True)


# Figure 3

plt.figure(figsize=(4,3))
Ls = np.linspace(0,L_max*np.pi/2,1000)
ws = w(Ls)
plt.plot(Ls,ws)
plt.plot([L_max*np.pi/2, L_max*np.pi/2],[0,1000],'--',color='grey')
plt.ylim(0,200)
plt.xlim(0,0.8*L_max*np.pi)
#plt.savefig('labor_supply.svg',transparent=True)


# Figure 4

a2s = [0.001, 10, 12.5, 15]
plt.figure(figsize=(4,3))
color_cycle = plt.gca()._get_lines.prop_cycler
colors = [next(color_cycle)['color'] for _ in range(10)]
Ls = np.linspace(0,300,1000)
for i, a2 in enumerate(a2s):
	Pis = f(K,Ls,a1,a2) - w(Ls)*Ls
	max_index = np.nanargmax(Pis)
	L_star = Ls[max_index]
	Pi_star = Pis[max_index]
	plt.plot(Ls,Pis,color=colors[i])
	plt.plot(L_star,Pi_star,'o',color=colors[i],markersize=8)
plt.ylim(750,1600)
plt.xlim(-1,200)
#plt.savefig('Pi_vs_L.svg',transparent=True)
plt.show()




