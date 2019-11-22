import numpy as np

import matplotlib.pyplot as plt
from scipy import stats
import math

def modified_thompson_tau(n):
      t_stud = stats.t.ppf(1-0.025, n-2)
      tau = t_stud * (n-1) / ( math.sqrt(n) * math.sqrt(n-2 + t_stud**2 ))
      return tau


tiempo_total= []
archivoRTTs = open('./ips_rtts','r+')
for l in archivoRTTs:
    tiempo_total.append(np.mean(list(map(float,l[:-1].split(',')[1:]))))

tiempo_por_salto = []
label_por_salto = []
archivo = open('./tiempos_saltos','r')
#mean y std una vez descartados outliers
tiempo_mean,tiempo_std,cant_outliers = list(map(float,archivo.readline()[:-1].split(',')))
for l in archivo:
    label_por_salto.append(l[:-1].split(',')[0] + '\n' + l[:-1].split(',')[1])
    tiempo_por_salto.append(float(l[:-1].split(',')[2]))

# plt.plot([tiempo_mean] * len(tiempo_por_salto),'y--',label='media sin outliers')
# plt.plot([tiempo_mean + 2 * tiempo_std] * len(tiempo_por_salto),'c--' ,label='media + 2 * std sin outliers')
# plt.plot([x for x in range(len(tiempo_por_salto))],tiempo_por_salto, 'ro', label='RTT entre saltos')
#
# plt.xticks([x for x in range(len(tiempo_por_salto))], label_por_salto, rotation=45)
# plt.subplots_adjust(bottom=0.15)
# #plt.axis(label_por_salto)
# plt.legend()
# plt.show()


#grafico rtt entre salto barras
y_pos = np.arange(len(tiempo_por_salto))



plt.bar(y_pos, tiempo_por_salto, align='center', alpha=0.5,label= 'RTT entre Saltos')
#plt.plot([tiempo_mean] * len(tiempo_por_salto),'y--',label='media sin outliers')
#plt.plot([tiempo_mean + 2 * tiempo_std] * len(tiempo_por_salto),'c--' ,label='media + 2 * std sin outliers')
plt.xticks(y_pos, label_por_salto,rotation=45)
plt.ylabel('tiempo (s)')
plt.title('RTT entre saltos')
plt.axhline(0, color='black')
plt.axhline(tiempo_mean, color='y',ls='--',label='mean (mean sin outliers)')
plt.axhline(tiempo_mean + 2 * tiempo_std, color='c',ls='--',label='mean + 2 * S  (S,mean sin outliers)')
plt.plot(tiempo_total,color='grey',ls='-.',label='RTT por salto')
plt.subplots_adjust(bottom=0.15)
plt.legend()
plt.show()

tiempo_por_salto_sin0 = []
for i in  range(len(tiempo_por_salto)):
    if tiempo_por_salto[i] > 0 :
        tiempo_por_salto_sin0.append(tiempo_por_salto[i])
X_mean_inicial = np.mean(tiempo_por_salto_sin0)
x_std_inicial = np.std(tiempo_por_salto_sin0)
values_of_deviation_per_S_with_outliers = [(x_i - X_mean_inicial) / x_std_inicial for x_i in tiempo_por_salto ]
values_of_deviation_per_S_without_outliers = [(x_i - tiempo_mean) / tiempo_std for x_i in tiempo_por_salto ]
#plt.plot([tiempo_mean] * len(tiempo_por_salto),'y--',label='media sin outliers')
#plt.plot([tiempo_mean + 2 * tiempo_std] * len(tiempo_por_salto),'c--' ,label='media + 2 * std sin outliers')
# plt.plot([x for x in range(len(tiempo_por_salto))],values_of_deviation_per_S_with_outliers, 'co', label='xi - X / S con outliers')
# plt.plot([x for x in range(len(tiempo_por_salto))],values_of_deviation_per_S_without_outliers, 'ro', label='xi - X / S sin outliers')
# plt.plot([modified_thompson_tau(len(tiempo_por_salto))] * len(tiempo_por_salto),'c--',label='tau con outliers')
# plt.plot([modified_thompson_tau(len(tiempo_por_salto)-cant_outliers)] * len(tiempo_por_salto),'r--',label='tau sin outliers')
#
# plt.xticks([x for x in range(len(tiempo_por_salto))], label_por_salto, rotation=45)
# plt.subplots_adjust(bottom=0.15)
# #plt.axis(label_por_salto)
# plt.legend()
# plt.show()




# val_of_dev_w_outliers = np.array(values_of_deviation_per_S_with_outliers)
# val_of_dev_wo_outliers = np.array(values_of_deviation_per_S_without_outliers) - val_of_dev_w_outliers
#
#
# ind = np.arange(len(val_of_dev_w_outliers))    # the x locations for the groups
# width = 0.35       # the width of the bars: can also be len(x) sequence
#
# p1 = plt.bar(ind, val_of_dev_w_outliers, width, color='#d62728')
# p2 = plt.bar(ind, val_of_dev_wo_outliers, width, bottom=val_of_dev_w_outliers)
#
# plt.ylabel('Scores')
# plt.title('Scores by group and gender')
# plt.xticks(ind, label_por_salto,rotation=45)
# plt.axhline(0, color='black')
# #plt.legend((p1[0], p2[0]), ('Men', 'Women'))
#
# plt.show()



N = 5
val_of_dev_w_outliers = np.array(values_of_deviation_per_S_with_outliers)
val_of_dev_wo_outliers = np.array(values_of_deviation_per_S_without_outliers)


fig, ax = plt.subplots()

ind = np.arange(len(val_of_dev_w_outliers))    # the x locations for the groups
width = 0.35         # the width of the bars
p1 = ax.bar(ind, val_of_dev_w_outliers, width, bottom=0,label='(Xi - mean(X)) / S (S y mean con outliers)')


p2 = ax.bar(ind + width, val_of_dev_wo_outliers, width, bottom=0, label='(Xi - mean(X)) / S (S y mean sin outliers)')

ax.set_title('values of deviation / S')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(label_por_salto,rotation=45)

plt.axhline(0, color='black')
plt.axhline(modified_thompson_tau(len(tiempo_por_salto)) , color='blue',ls=':',label = 'M.T. tau (con outliers)')
plt.axhline(modified_thompson_tau(len(tiempo_por_salto)-cant_outliers), color='orange',ls='--',label = 'M.T. tau (sin outliers)')
ax.legend()
#ax.yaxis.set_units(inch)
#ax.autoscale_view()
plt.subplots_adjust(bottom=0.15)
plt.show()


#
# fig = plt.figure()
# x = np.arange(10)
# y = 2.5 * np.sin(x / 20 * np.pi)
# yerr = np.linspace(0.05, 0.2, 10)
#
# #plt.errorbar(x, y + 3, yerr=yerr, label='both limits (default)')
#
# #plt.errorbar(x, y + 2, yerr=yerr, uplims=True, label='uplims=True')
#
# plt.errorbar(x, y + 1, yerr=yerr, uplims=True, lolims=True, marker ='|',capsize=3,  label='saltos RTT')
#
# # upperlimits = [True, False] * 5
# # lowerlimits = [False, True] * 5
# # plt.errorbar(x, y, yerr=yerr, uplims=upperlimits, lolims=lowerlimits,
# #              label='subsets of uplims and lolims')
#
# plt.legend(loc='lower right')

#plt.show()
