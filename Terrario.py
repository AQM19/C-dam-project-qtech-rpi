class Terrario:
    def __init__(self, temperatura_media, temperatura_media_hiber, humedad_media, horas_luz, horas_luz_hiber):
        self.temperatura_media = temperatura_media
        self.temperatura_media_hiber = temperatura_media_hiber
        self.humedad_media = humedad_media
        self.horas_luz = horas_luz
        self.horas_luz_hiber = horas_luz_hiber
    
    def __str__(self):
        return "Terrario[temperatura_media={}, temperatura_media_hiber={}, humedad_media={}, horas_luz={}, horas_luz_hiber={}]".format(self.temperatura_media, self.temperatura_media_hiber, self.humedad_media, self.horas_luz, self.horas_luz_hiber)