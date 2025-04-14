import serial
import time

# Abrir puerto serie (COM20 a 115200 baudios, 8N1)
ser = serial.Serial('COM20', 115200, timeout=1)  # En Linux, seria '/dev/ttyUSB0' pero no lo pude aplicar


# Dar al módem algo de tiempo para reiniciarse o responder, esto es opcional pero con la 
# ESP-01s y el wifi fue mejor hacerlo 
time.sleep(2)  

# Enviar un comando AT para probar la comunicación
cmd = 'AT\r\n'                                  # Mandar comando y terminarlos con \r\n
ser.write(cmd.encode())                          # Enviar el comando
print(f"Sent: {cmd.strip()}")                    # mpstrar lo enviado


time.sleep(1)                                  # hago tiempo para esperar la respuesta
resp = ser.read_all().decode(errors='ignore')    # Leer todos los datos disponibles
print(f"Response: {resp}")                       # Leo la respuesta del modem


cmd = 'AT+CSQ\r\n'
ser.write(cmd.encode())
print(f"Sent: {cmd.strip()}")
time.sleep(0.5)
resp = ser.read_all().decode(errors='ignore')
print(f"Response: {resp}")


cmd = 'AT+CEREG?\r\n'
ser.write(cmd.encode())
print(f"Sent: {cmd.strip()}")
time.sleep(0.5)
resp = ser.read_all().decode(errors='ignore')
print(f"Response: {resp}")



# Configuracion de SMS
# Para poder enviar, recibir o verificar SMS se debe usar el comando "AT+CMGF=1" en el caso de no usarlo no se podra utilizar la funcion
cmd = 'AT+CMGF=1\r\n'
ser.write(cmd.encode())
print(f"Sent: {cmd.strip()}")
time.sleep(0.5)
resp = ser.read_all().decode(errors='ignore')
print(f"Response: {resp}")


# AT+CPMS? Comando para verificar el buffer de memoria 
cmd = 'AT+CPMS?\r\n'
ser.write(cmd.encode())
print(f"Sent: {cmd.strip()}")
time.sleep(0.5)
resp = ser.read_all().decode(errors='ignore')
print(f"Response: {resp}")

"""
Si nos hubiera indicado 
+CPMS: "ME",23,23,"ME",23,23,"ME",23,23

Indica memoria llena, en esta caso no puede recibir mas mensajes de texto.
Para limpiar la memoria se debe usar el comando "AT+CMGD=1,4" dejando el codigo

cmd = 'AT+CMGD=1.4\r\n'
ser.write(cmd.encode())
print(f"Sent: {cmd.strip()}")
time.sleep(0.5)
resp = ser.read_all().decode(errors='ignore')
print(f"Response: {resp}")

Si nos devuelve OK indica que la ejecucion esta bien

"""

# Ver Todos los SMS de la placa 
cmd = 'AT+CMGL="ALL"\r\n'
ser.write(cmd.encode())
print(f"Sent: {cmd.strip()}")
time.sleep(1)
resp = ser.read_all().decode(errors='ignore')
print(f"Response: {resp}")


# ENVIO SMS



#Ejemplo de SMS con Arreglo
arreglo=[20, 40, 10]


numero_destino = "3582649734"
cmd = f'AT+CMGS="{numero_destino}"\r\n'
ser.write(cmd.encode())
time.sleep(1)
resp = ser.read_all().decode(errors='ignore')
print("CMGS Response:", resp)

if '>' in resp:
    #    Importante: no poner \r\n aquí, sino directamente \x1A
    # Envías primera línea de texto
    ser.write(b"Hola Tomi desde BG96 con Python\r\n")
    time.sleep(0.2)
    
    # Envías la línea con el valor de arreglo[0]
    ser.write(f"Temperatura: {arreglo[0]}\r\n".encode())
    time.sleep(0.2)
    
    # Envías la línea con el valor de arreglo[1]
    ser.write(f"Presión: {arreglo[1]}\r\n".encode())
    time.sleep(0.2)

    # Envías la línea con el valor de arreglo[2]
    ser.write(f"Humedad: {arreglo[2]}\r\n".encode())
    time.sleep(0.2)
    
    # Control+Z para finalizar el mensaje
    ser.write(b"\x1A")  
    time.sleep(0.5)

    # 5) Leer la respuesta a ver si se envió bien
    resp_sms = ser.read_all().decode(errors='ignore')
    print("Send SMS Resp:", resp_sms)
    # Normalmente verás algo como:
    # +CMGS: <ID>
    # OK
else:
    print("No se recibió el prompt '>'; no se pudo enviar el texto.")



ser.close()