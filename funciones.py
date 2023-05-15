import minimalmodbus, serial, datetime, json

# Puertos e IDs

puerto = 'COM8'
id1 = 1
id2 = 3

# Direcciones y claves

keys1 = ["array_current1", "array_voltage1", "array_power1", "battery_voltage1", 
        "battery_current1", "battery_SOC1", "battery_temp1", "regulator_temp1", 
        "load_current1", "load_voltage1", "load_power1", "load_status1"]

keys2 = ["array_current2", "array_voltage2", "array_power2", "battery_voltage2", 
        "battery_current2", "battery_SOC2", "battery_temp2", "regulator_temp2", 
        "load_current2", "load_voltage2", "load_power2", "load_status2"]
        
dir = [0x3101, 0x3100, 0x3102, 0x331A, 0x331B, 0x311A, 
        0x3110, 0x3111, 0x310D, 0x310C, 0x310E, 0x3202]

# Validar instrumento 

def validar_instrumento(puerto, id):
    try:
        # Se crea instrumento para cada regulador
        instrument = minimalmodbus.Instrument(puerto, id, minimalmodbus.MODE_RTU)
    except minimalmodbus.ModbusException as e:
        return None
    except serial.SerialException as e:
        return None
    else:
        return instrument

# Crear diccionario

def crear_dic(instrument1, instrument2, keys1, keys2, dir):
    
    data_dict = {}
    now = datetime.datetime.now()
    fecha_hora = now.strftime("%d/%m/%Y %H:%M:%S")
    data_dict["fecha_hora"] = fecha_hora
            
    for i in range(len(dir)):
        try:
            if keys1[i] == "battery_SOC1" or keys1[i] == "load_status1":
                var1 = instrument1.read_register(dir[i], functioncode=4)
            elif keys1[i] == "battery_current1":
                var1 = (-1)*((instrument1.read_register(dir[i], functioncode=4) - 65000) / 100)
            else:
                var1 = instrument1.read_register(dir[i], functioncode=4)/100
        except:
            var1 = ""
        data_dict[keys1[i]] = var1

    for i in range(len(dir)):
        try:
            if keys2[i] == "battery_SOC2" or keys2[i] == "load_status2":
                var2 = instrument2.read_register(dir[i], functioncode=4)
            elif keys2[i] == "battery_current2":
                var2 = (-1)*((instrument2.read_register(dir[i], functioncode=4) - 65000) / 100)
            else:
                var2 = instrument2.read_register(dir[i], functioncode=4)/100
        except:
            var2 = ""
        data_dict[keys2[i]] = var2
    
    return data_dict

# Diccionario vacio

def vacio(keys):

    data_dict = {}
    now = datetime.datetime.now()
    fecha_hora = now.strftime("%d/%m/%Y %H:%M:%S")
    data_dict["fecha_hora"] = fecha_hora

    for i in range(len(keys)):
        data_dict[keys[i]] = ""
    
    return data_dict

# Enviar diccionario

def enviar_dict(ser, data_dict):
    json_data = json.dumps(data_dict)
    bytes_data = json_data.encode()
    ser.write(bytes_data)

# Baudrate y timeout

def parametros(Instrument):
    Instrument.serial.baudrate = 115200
    Instrument.serial.timeout = 1

# Leer los datos

def leer_datos(InstrumentA, InstrumentB):
    parametros(InstrumentA)
    parametros(InstrumentB)
    data_dict = crear_dic(InstrumentA, InstrumentB, keys1, keys2, dir)    
    return data_dict