-La carpeta capturas tiene las capturas (en formato csv) de los RTTs de las 3 rutas analizadas
-La carpeta codigo tiene:
	-tracerouteICMP.py , este genera las capturas de RTT en formato csv, pero no es necesario llamarlo explicitamente ya que se ejecuta indirectamente desde 'ejercicioAyB.py', la ruta a analizar hay que si escribirla a mano en este archivo
	-ejercicioAyB.py , este archivo da la opcion de utilizar una captura vieja o realizar denuevo el traceroute (ejecutar tracerouteICMP.py) y luego realizar lo pedido por los ejercicios A y B.
si se correr un nuevo traceroute el stdoutput del tracerouteICMP esta redirigido a un archivo de log para poder analizar los paquetes enviados o debuggear.
	-dibujar_mapa.py , este archivo dibuja mapas a partir de Ips. Es necesario ya haber ejecutado el ejercicioAyB.py
	-graficosRTT.py , este archivo plotea los graficos utilizados en el informe, es necesario haber 

-La carpeta graficos contiene los graficos generados tanto por graficosRTT.py como los mapas generados por dibujar_mapa.py
