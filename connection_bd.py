import mysql.connector
from Terrario import Terrario

class ConnectionBD:
    def __init__(self):
        self.hostname = 'qtech.mysql.database.azure.com'
        self.username = 'aaronibio'
        self.password = 'AqMr190216'
        self.database = 'qtech'
        self.connection = None
        self.connected = False

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.hostname,
                user=self.username,
                password=self.password,
                database=self.database
            )
            print('Conexión exitosa a la base de datos')
            self.connected = True
        except mysql.connector.Error as error:
            print('Error al conectarse a la base de datos: {}'.format(error))
    
    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connected = False
            print('Desconexion exitosa de la base de datos')
    
    def is_connected(self):
        return self.connected
    
    def insert_lectura(self, lectura):
        if self.connection:
            try:
                cursor = self.connection.cursor()

                sql = "INSERT INTO lecturas (idterrario, fecha, temperatura, humedad, luz) VALUES (%s, %s, %s, %s, %s)"
                values = (lectura.idterrario, lectura.fecha, lectura.temperatura, lectura.humedad, lectura.luz)

                cursor.execute(sql, values)
                self.connection.commit()
                
                print('Lectura insertada correctamente en la base de datos')
            except mysql.connector.Error as error:
                print('Error al insertar la lectura en la base de datos: {}'.format(error))

    def read_terra(self):
        if self.connection:
            try:
                cursor = self.connection.cursor()
                
                sql = """
                SELECT
                (temperatura_minima + temperatura_maxima) / 2 as temperatura_media,
                (temperatura_minima_hiber + temperatura_maxima_hiber) / 2 as temperatura_media_hiber,
                (humedad_minima + humedad_maxima) / 2 as humedad_media,
                horas_luz, horas_luz_hiber
                FROM terrarios
                WHERE id = 4;
                """
                
                cursor.execute(sql)
                
                result = cursor.fetchone()
                
                terrario = Terrario(result[0], result[1], result[2], result[3], result[4])
                
                return terrario
                
            except Exception as e:
                print("Error:", e)