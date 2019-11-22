import subprocess
import random
print('queres correr un traceroute nuevo (S/N). Sino pones N se utiliza a ultima captura: ')
if input()=='S':
    archivo_log = open('log_traceroute.txt','w')
    print('Espera a que se realice el traceroute (puede tardar)')
    subprocess.call(['sudo','python2.7', 'tracerouteICMP.py'],stdout=archivo_log)

import numpy as np
from scipy import stats
import math

def modified_thompson_tau(n):
    #Studnt, n=999, p<0.05, 2-tail
    #equivalent to Excel TINV(0.05,999)
    #print stats.t.ppf(1-0.025, 999)
      t_stud = stats.t.ppf(1-0.025, n-2)
      tau = t_stud * (n-1) / ( math.sqrt(n) * math.sqrt(n-2 + t_stud**2 ))
      return tau

#labels son los nombres o la manera de referirse a cada muestra, no puedo usar i (nro de muestra por que la voy cambiando)
#labels pueden ser las ips o una  simplement una lista [0,1,2,3,4,5,6,...]
def detectar_outliers(X,labels):
    X_sin0 = []
    labels_sin0 = []
    for i in  range(len(X)):
        if X[i] > 0 :
            X_sin0.append(X[i])
            labels_sin0.append(labels[i])
    X[:] = X_sin0
    labels[:] = labels_sin0
    X_mean = np.mean(X)
    S_std = np.std(X)
    tau = modified_thompson_tau(len(X))
    # print('X_mean ',X_mean)
    # print('tau * S: ',tau * S_std)
    deltas = []
    for x_i in X:
        #delta_i = abs(x_i - X_mean) para detectar outliers el metodo propuesto calcula los delta_i de este modo sin embargo a mi solo me importan los outliers que se pasen de grandesn, no de chicos
        delta_i = x_i - X_mean
        deltas.append(delta_i)

    # print('labels:  ',labels)
    # print('deltas ' , deltas)
    i_max = deltas.index(max(deltas))
    if deltas[i_max] > tau * S_std:
        label_outlier_encontrado = labels[i_max]
        X.pop(i_max)
        labels.pop(i_max)
        return  [label_outlier_encontrado] + detectar_outliers(X,labels)
    else:
        return []


ips = ['start']
ip_rtts = {"start" : [0]}
archivo = open('./ips_rtts','r')
#iprouter = archivo.readline() esta linea la descomento si no quiero tener en cuenta el router
for l in archivo:
    ips.append(l.split(',')[0])
    ip_rtts[l.split(',')[0]] =list( map(float , l[:-1].split(',')[1:]) )

# print('ips:')
#print('ips: ',ips)
# print('ip_rtts')
# print(ip_rtts)

tiempos_prom_saltos = [] #habria que poner [0] para decir que llegar a star cuesta 0?

for destino in range(1,len(ips)):
    tiempos_prom_saltos.append(np.mean(np.array(ip_rtts[ips[destino]]))-np.mean(np.array(ip_rtts[ips[destino -1]])) )

#todos los saltos negativos los mando a 0 porque fisicamente es imposible
tiempos_prom_saltos = list(map(lambda x: x if x > 0 else 0 ,tiempos_prom_saltos))
# print('saltos tiempo')
# print(tiempos_prom_saltos)
# print('-------------------------')
print('Aumento RTT por salto')
print('ip' + '          ' + 'salto de rtt' + '          ' + 'RTT')
print(ips[0] + "          " + str(0) + "          "  + str(0))
for i in range(1,len(ips)):
    print(ips[i] + "          " + str( tiempos_prom_saltos[i-1]) + "          " + str(np.mean(np.array(ip_rtts[ips[i]])) ) )

#ACA ARRANCA EL EJ B , PREDICCION  POR DETECCION DE OUTLIERS
print('--------------------')

X_mean = np.mean(tiempos_prom_saltos)
S_std = np.std(tiempos_prom_saltos)
# print('media saltos: ' + str(X_mean) )
# print("std saltos: " + str(S_std))

tiempos_prom_saltos_copia = tiempos_prom_saltos.copy()
outliers = detectar_outliers(tiempos_prom_saltos_copia, ips.copy()[1:])
print('outliers', outliers)

print('enlaces intercontinentales: ')
for out in outliers:
    print('hay enlace intercontinental entre: ' + ips[ips.index(out)-1] + ' y ' + out)


#guardo en csv los saltos de tiempos

archivo = open('./tiempos_saltos','w+')
archivo.write(str(np.mean(tiempos_prom_saltos_copia))+','+str(np.std(tiempos_prom_saltos_copia))+','+ str(len(outliers))+ '\n')
for i in range(len(ips)-1):
    archivo.write(ips[i] + ',' + ips[i+1] +','+ str(tiempos_prom_saltos[i]) + '\n')
