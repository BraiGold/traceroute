from scapy.all import *

from time import *

host_destino = 'www.helsinki.fi'#'www.unisa.ac.za'#'www.univ-antananarivo.mg'#'www.unsw.edu.au' #'vnu.edu.vn' #'www.technion.ac.il' #'www.weizmann.ac.il'
traceroute(host_destino)
minttl = 1
maxttl = 30
ip_pos = {}
ip_rtts_list = []
ips = []
for tiempo in range(minttl,maxttl):
    paquetes_por_ttl = 30
    for nro_rafaga in range(paquetes_por_ttl):
        a,b = sr(IP(dst=host_destino, id=RandShort(), ttl=tiempo)/ICMP(id=RandShort(),seq=RandShort()), timeout=2)
        for nro_paquete in range(len(a[ICMP])):
            #el 1 de abajo indica que estoy hablando de la respuesta, el 0 seria el mensaje enviado
            paq_enviado = a[ICMP][nro_paquete][0]
            paq_recibido = a[ICMP][nro_paquete][1]
            rtt = paq_recibido.time - paq_enviado.sent_time
            ipResupuesta = paq_recibido.src
            #timeout por tll agotado es codigo 11
            codigo_respuesta = paq_recibido.type

            if ipResupuesta in ip_pos:
                ip_rtts_list[ip_pos[ipResupuesta]].append(rtt)
            else:
                ip_pos[ipResupuesta] = len(ip_rtts_list)
                ip_rtts_list.append([rtt])
                ips.append(ipResupuesta)

            #pa testestar
            a.summary()
            print "paquete " + str(nro_paquete)
            print 'src: '
            print a[ICMP][nro_paquete][1].src
            print 'dst:     '
            print a[ICMP][nro_paquete][1].dst
            print a[ICMP][nro_paquete][1].type

print ip_pos
print ip_rtts_list

#escribo en archivo csv los resultados:
archivo = open('./ips_rtts','w+')
for ip in ips:
    archivo.write(ip)
    for e_rtt in ip_rtts_list[ip_pos[ip]]:
        archivo.write(',' + str(e_rtt))
    archivo.write('\n')


# print 'resultado de traceroute: '
# for ip in ips:
#     print ip + str(statistics.mean(ip_rtts_list[ip_pos[ip]]))
