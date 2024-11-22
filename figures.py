import numpy as np
import matplotlib.pyplot as plt


class Model():
    def __init__(self, A_old, A_auto, alpha, gamma, w_min, L_max, Kbar):
        self.A_old = A_old
        self.A_auto = A_auto
        self.alpha = alpha
        self.gamma = gamma
        self.w_min = w_min
        self.L_max = L_max
        self.Kbar = Kbar

    def f(self, K, L):
        K1 = np.minimum(L*(self.alpha*self.A_old/self.A_auto)**(1/(1-self.alpha)), K*np.ones_like(L))
        return self.A_old*K1**self.alpha*L**(1-self.alpha) + self.A_auto*(K-K1)

    def w(self, L):
        return self.w_min/(1 - L/(gamma*self.L_max))

    def outcomes(self):
        L_list = np.linspace(0, self.L_max*gamma*0.99999, 10000)
        f_list = self.f(self.Kbar, L_list)
        Pi_list = f_list - self.w(L_list)*L_list
        max_index = np.nanargmax(Pi_list)
        L_star = L_list[max_index]
        f_star = f_list[max_index]
        Pi_star = Pi_list[max_index]
        K1_star = min([L_star*(self.alpha*self.A_old/self.A_auto)**(1/(1-self.alpha)), self.Kbar])
        w_star = self.w(L_star)
        return L_star, f_star, Pi_star, K1_star, w_star


# Specificying model parameters:
L_max = 500
w_min = 2
alpha = 0.5
A_old = 3.088  # Set so that Cap_Prod0 = 1
Kbar = 50
gamma = 0.5


# Max value of A_auto for plots.
A_auto_max = 3


model = Model(A_old, 0.0001, alpha, gamma, w_min, L_max, Kbar)

A_autos = np.linspace(0.001, A_auto_max, 500)
Ls = np.zeros_like(A_autos)
fs = np.zeros_like(A_autos)
Pis = np.zeros_like(A_autos)
K1s = np.zeros_like(A_autos)
ws = np.zeros_like(A_autos)

# Computing the initial marginal product of capital
# A_old is set so this equals 1
L0, _, _, _, _ = model.outcomes()
Cap_Prod0 = A_old*alpha*Kbar**(alpha-1)*L0**(1-alpha)

# Solve model at each value of A_auto
for i, A_auto in enumerate(A_autos):
    model.A_auto = A_auto
    Ls[i], fs[i], Pis[i], K1s[i], ws[i] = model.outcomes()


"""

Figure 2:

"""
fig, axes = plt.subplots(2, 2, figsize=(10, 5))
linewidth = 2

# Production
axes[0, 0].plot(A_autos, fs, color='#2a9d8f', linewidth=linewidth)
axes[0, 0].spines[['right', 'top']].set_visible(False)
axes[0, 0].set_xlim(0, 2.5)
axes[0, 0].set_ylim(0, 125)
axes[0, 0].set_yticks([0, 50, 100])
axes[0, 0].set_xticks([0, 1, 2])

# Capital Allocation
axes[0, 1].plot(A_autos, 100*(Kbar-K1s)/Kbar, color='#c1121f', linewidth=linewidth)
axes[0, 1].plot(A_autos, 100*K1s/Kbar, color='#669bbc', linewidth=linewidth)
axes[0, 1].spines[['right', 'top']].set_visible(False)
axes[0, 1].set_xlim(0, 2.5)
axes[0, 1].set_ylim(-0.6, 101)
axes[0, 1].set_yticks([0, 50, 100])
axes[0, 1].set_xticks([0, 1, 2])

# Firm's profits
axes[1, 0].plot(A_autos, Pis, color='#2a9d8f', linewidth=linewidth)
axes[1, 0].spines[['right', 'top']].set_visible(False)
axes[1, 0].set_xlim(0, 2.5)
axes[1, 0].set_ylim(0, 125)
axes[1, 0].set_yticks([0, 50, 100])
axes[1, 0].set_xticks([0, 1, 2])

# Labor Employment
axes[1, 1].plot(A_autos, Ls, color='#2a9d8f', linewidth=linewidth)
axes[1, 1].spines[['right', 'top']].set_visible(False)
axes[1, 1].set_xlim(0, 2.5)
axes[1, 1].set_ylim(-0.6*25/100, 25)
axes[1, 1].set_xticks([0, 1, 2])

plt.subplots_adjust(wspace=0.4, hspace=0.4)


"""

Figure 1B:

"""
xlim = [0, 1.4*L_max/2]
ylim = [0, 50]
plt.figure(figsize=(2.3, 2.5))
Ls = np.linspace(0, L_max/2, 1000)
ws = model.w(Ls)
plt.plot(Ls, ws)
plt.plot([L_max/2, L_max/2], [0, 1000], '--', color='grey')
plt.ylim(ylim)
plt.xlim(xlim)
plt.gca().spines[['right', 'top']].set_visible(False)
plt.gca().set_xticks([L_max/2])
plt.gca().set_yticks([0, 10*w_min, 20*w_min])


"""

Figure 1C:

"""
A_autos = [0.001, 1, 1.1, 1.2]
plt.figure(figsize=(3, 2.7))
color_cycle = plt.gca()._get_lines.prop_cycler
colors = [next(color_cycle)['color'] for _ in range(10)]
Ls = np.linspace(-1, 100, 1000)
for i, A_auto in enumerate(A_autos):
    model.A_auto = A_auto
    Pis = model.f(Kbar, Ls) - model.w(Ls)*Ls
    max_index = np.nanargmax(Pis)
    L_star = Ls[max_index]
    Pi_star = Pis[max_index]
    plt.plot(Ls, Pis, color=colors[i])
    plt.plot(L_star, Pi_star, 'o', color=colors[i], markersize=8)
plt.ylim(40, 62)
plt.xlim(-.2, 30)
plt.gca().spines[['right', 'top']].set_visible(False)

plt.show()
