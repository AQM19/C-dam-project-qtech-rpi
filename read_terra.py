import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import gpiozero
import datetime

from connection_bd import ConnectionBD
from Lectura import Lectura

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN)

RELAY_PIN17 = 17
RELAY_PIN27 = 27
RELAY_PIN22 = 22

manta = gpiozero.OutputDevice(RELAY_PIN17, active_high=False, initial_value=False)
agua = gpiozero.OutputDevice(RELAY_PIN27, active_high=False, initial_value=False)
luz = gpiozero.OutputDevice(RELAY_PIN22, active_high=False, initial_value=False)

pin = 4
sensor = Adafruit_DHT.DHT11
interval = 1

timenow = datetime.datetime.now().time()
inicio_noche = datetime.time(22, 0)
fin_noche = datetime.time(8, 0)

datenow = datetime.datetime.now().date()
inicio_invierno = datetime.date(datenow.year, 12, 1)
fin_invierno = datetime.date(datenow.year + 1, 3, 1)

conexion = ConnectionBD()
conexion.connect()

lecturas = []
buffer = []

def insert_media():
    global lecturas
    sum_temperatura = sum(lect.temperatura for lect in lecturas)
    sum_humedad = sum(lect.humedad for lect in lecturas)
    sum_luz = sum(lect.luz for lect in lecturas)

    media_temperatura = sum_temperatura / len(lecturas)
    media_humedad = sum_humedad / len(lecturas)
    media_luz = sum_luz / len(lecturas)

    media_lectura = Lectura(media_temperatura, media_humedad, media_luz)
    buffer.append(media_lectura)

    lecturas = []
    
def es_de_noche():
    global timenow, inicio_noche, fin_noche
    
    if inicio_noche <= timenow or timenow <= fin_noche:
        return True
    else:
        return False
    
def es_invierno():
    global datenow, inicio_invierno, fin_invierno
    
    if inicio_invierno <= datenow < fin_invierno:
        return True
    else:
        return False

def insert_buffer():
    global buffer
    try:
        for media in buffer:
            conexion.insert_lectura(media)
        buffer.clear()
        print('Datos enviados correctamente')
    except Exception as e:
        print('Error al enviar los datos:', str(e))
        
def set_relay(status, relay):
    if status:
        relay.on()
    else:
        relay.off()
        
def control_terra(lectura):
    if es_invierno():
        if lectura.temperatura >= terrario.temperatura_media_hiber:
            set_relay(False, manta)
        else:
            set_relay(True, manta)
            
        if es_de_noche() == False:
            if lectura.luz >= terrario.horas_luz_hiber:
                set_relay(False, luz)
            else:
                set_relay(True, luz)
    else:
        if lectura.temperatura >= terrario.temperatura_media:
            set_relay(False, manta)
        else:
            set_relay(True, manta)
            
        if es_de_noche() == False:
            if lectura.luz >= terrario.horas_luz:
                set_relay(False, luz)
            else:
                set_relay(True, luz)
        
    if lectura.humedad >= terrario.humedad_media:
        set_relay(False, agua)
    else:
        set_relay(True, agua)

set_relay(False, manta)
set_relay(False, agua)
set_relay(False, luz)

while True:
    terrario = conexion.read_terra()
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    light = GPIO.input(17)
    
    lectura = Lectura(temperature, humidity, light)
    lecturas.append(lectura)
    
    if terrario is not None:
        control_terra(lectura)        
    
    if len(lecturas)==6:
        insert_media()
    
    if len(buffer)>0:
        if conexion.is_connected():
            insert_buffer()
    
    print(lectura.__str__())
    time.sleep(interval)