from datetime import datetime

class Lectura:
    def __init__(self, temperatura, humedad, luz):
        self.idterrario = 4
        self.fecha = datetime.now()
        self.temperatura = temperatura
        self.humedad = humedad
        self.luz = luz
        
    def __str__(self):
        return "Lectura[temperatura={}, humedad={}, luz={}]".format(self.temperatura, self.humedad, self.luz)