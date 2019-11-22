from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from ip2geotools.databases.noncommercial import DbIpCity
from matplotlib.pyplot import cm
import numpy as np
from random import seed
from random import random
from random import randint

seed(2)
ips = []
archivo = open('./ips_rtts','r')
iprouter = archivo.readline()
for l in archivo:
    ips.append(l.split(',')[0])


print(ips)


m = Basemap(projection='robin',lon_0=0, llcrnrlat=-60, llcrnrlon = -180, urcrnrlat = 90, urcrnrlon = 180, resolution = 'l')

#m.drawcoastlines()
#m.drawcountries(linewidth=1)
#m.drawstates(color='b')
m.bluemarble()

#color=iter(cm.rainbow(np.linspace(0,1,4)))
#c=next(color)
#plt.plot(x,y,c=c)
#ips = ['201.231.138.102','120.45.60.3','8.8.8.8','200.90.30.3','30.55.85.102']
#A arracna con la primer ip
#marcadores=['X','o','*','D']
response = DbIpCity.get(ips[0], api_key='free')
puntoAlat,puntoAlon = response.latitude, response.longitude
if puntoAlat is None or puntoAlon is None:
    print('la api no funciono, tendra que cargar el punto de partida a mano ')
    print('ingresa  lat y lon (en ese orden) de: ' + ips[0] )
    puntoAlat = float(input())
    puntoAlon = float(input())
xpt,ypt = m(puntoAlon,puntoAlat)
m.plot(xpt,ypt,color=(random(),random(),random(),1),marker='X',ms=9,label='start')
for i in range(len(ips)-1):
    try:
        response = DbIpCity.get(ips[i+1], api_key='free')
    except:
        print("!!!!!!! no anda la api !!!!!!!!!!")
    puntoBlat,puntoBlon = response.latitude, response.longitude


    print(ips[i+1])
    print(puntoAlon,puntoAlat)
    print(puntoBlon,puntoBlat)
    if puntoBlat is None or puntoBlon is None:
        print('la api no funciono desea omitir este punto o cargarlo a mano? escriba \'omitir\' o \'mano\' ')
        if(input() != 'omitir'):
            print('ingresa  lat y lon (en ese orden) de: ' + ips[i+1] )
            puntoBlat = float(input())
            puntoBlon = float(input())
        else:
            continue
    xpt,ypt = m(puntoBlon,puntoBlat)
    m.drawgreatcircle(puntoAlon,puntoAlat,puntoBlon,puntoBlat)

    m.plot(xpt,ypt,color=(random(),random(),random(),1),marker='X',ms=9,label=ips[i+1])
    puntoAlat,puntoAlon = puntoBlat,puntoBlon

plt.title('mapa traceroute')
plt.legend()
plt.show()
