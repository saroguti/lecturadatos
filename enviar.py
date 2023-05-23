import time, threading, funciones, serial, csv

# Archivo .csv

datos = 'C:\Users\Usuario\Desktop\Santiago\lecturadatos\datos.csv'

# Se crea el diccionario

data_dict = {}

# Serial

#ser = serial.Serial(port='/tmp/COM10', baudrate=115200)

# Se encarga de actualizar los datos de data_dict

def actualizar_datos():
    global data_dict
    instrument1, instrument2 =  None, None
    while True:
        if instrument1 == None:
            data_dict = funciones.vacio(funciones.keys1)
            data_dict |= funciones.vacio(funciones.keys2)
            instrument1 = funciones.validar_instrumento(funciones.puerto, funciones.id1)
            continue
        if instrument2 == None:
            data_dict = funciones.vacio(funciones.keys1)
            data_dict |= funciones.vacio(funciones.keys2)
            instrument2 = funciones.validar_instrumento(funciones.puerto, funciones.id2)
            continue
        try:
            data_dict = funciones.leer_datos(instrument1, instrument2)
        except Exception:
            data_dict = funciones.vacio(funciones.keys1)
            data_dict |= funciones.vacio(funciones.keys2)
            instrument1.serial.close()
            instrument2.serial.close()

# Funcion destinada a enviar los datos contenidos en data_dict
# Utilizar función enviar_dict de archivo funciones dentro de enviar_datos

# def enviar_datos():
#     while True:
#         print(data_dict)
#         time.sleep(5)
#         #funciones.enviar_dict(ser, data_dict)

def guardar_csv():
    while True:
        with open(datos, 'w', newline='') as file:
            # Crear el objeto escritor CSV
            writer = csv.DictWriter(file, fieldnames=data_dict.keys())

            # Escribir la fila de encabezado con las claves del diccionario
            writer.writeheader()

            # Escribir los datos del diccionario en el archivo CSV
            writer.writerow(data_dict)

# Se crean los hilos

t1 = threading.Thread(target=actualizar_datos)

t2 = threading.Thread(target=guardar_csv)

#t2 = threading.Thread(target=enviar_datos)

# Se inician los hilos

t1.start()

t2.start()
