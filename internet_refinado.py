#Se importan las librerías a utilizar y los scripts para el envío de datos
import time
import RPi.GPIO as GPIO
import requests
from RFM9X import RFM9X
from datetime import datetime
from sensordetemperatura import DS18B20
from sensordenivel import SRO4M
from turbidez import Turbidez
from Atlas import Atlas
rfm9x = RFM9X()
sensorNTU = Turbidez(configured_measurements = ["UNT"])
sensorAtlas = Atlas()
sensorNivel = SRO4M(configured_measurements = ["WaterLevel"])
sensorTemp = DS18B20(configured_measurements = ["Temperature"])
#Se inicializan los parámetros de medición de calidad de agua
NTU = 0
Solidos = 0
Nivel = 0
pH = 0
Temperatura = 0
Flujo = 0
Conductividad = 0
Salinidad = 0
while True:
    #Se realizan los llamados a las funciones de lectura de los parámetros
    contador = 0
    try:
        Temperatura = sensorTemp.read()[0]
    except:
        Temperatura = 0
        pass
    try:
        Nivel = sensorNivel.measure_distance()
    except:
        Nivel = 0
        pass
    try:
        NTU = sensorNTU.read()
    except:
        NTU =0
        pass
    try:
        pH = sensorAtlas.read()[0]
    except:
        pH = 0
        pass
    try:
        Solidos, Conductividad, Salinidad = sensorAtlas.read()[1:3]
    except:
        Solidos, Conductividad, Salinidad = 0,0,0
        pass
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    print(dt_string)
    #Se envían los elementos del diccionario compuesto por las mediciones obtenidas
    #send = {"id_device": str(21), "created_at": str(dt_string), "Turbidity":str(NTU), "DissolvedSolids":str(Solidos), "WaterLevel":str(Nivel), "pH":str(pH), "Temperature":str(Temperatura), "Flow":str(Flujo), "Conductivity":str(Conductividad), "Salinity":str(Salinidad)}
    send = "{},{},{},{},{},{},{},{},{},{}".format(21, dt_string, NTU, Solidos, Nivel, pH, Temperatura, Flujo, Conductividad, Salinidad)
    ack = rfm9x.send(str(send),50, with_ack = True)
    print(str(send))
    #Se utiliza un ciclo para revisar si se puede establecer las conexiones entre módulos LoRa
    while ack == False:
        if contador > 10:
            print("No se pudo realizar la conexion")
            break
        ack = rfm9x.send(str(send),50, with_ack = True)
        contador+=1
        time.sleep(1)
    time.sleep(20.0)
