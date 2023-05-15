import time, threading, funciones

# Se crea el diccionario

data_dict = {}

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

def enviar_datos():
    while True:
        print(data_dict)
        time.sleep(5)

# Se crean los hilos

t1 = threading.Thread(target=actualizar_datos)

t2 = threading.Thread(target=enviar_datos)

# Se inician los hilos

t1.start()

t2.start()
