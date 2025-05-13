import serial
import time

# Los datos enviados por modulos lora recibidos por la esp-32 son visto desde el 
# el serial monitor "COM17" y son procesados por este programa para ser enviados 
# por el modem BG96

#ser _ Serial al Modem BG96
#sout _ Serial a la esp32 conectada al Lora

ser = serial.Serial('COM27', 115200, timeout=1) 
sout= serial.Serial("COM17", 115200) #Salida del serial monitor con la esp-32 a Lora

# Dar al módem algo de tiempo para reiniciarse o responder, esto es opcional pero con la 
time.sleep(2)  

# Enviar un comando AT para probar la comunicación
cmd = 'AT\r\n'                      
ser.write(cmd.encode())                        
print(f"Sent: {cmd.strip()}")                    


time.sleep(1)                                  
resp = ser.read_all().decode(errors='ignore')   
print(f"Response: {resp}")                       


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


while(True):    
    try:
        while True:
            time.sleep(10)
            if sout.in_waiting:
                linea = sout.readline().decode(errors='ignore').strip()
                text=linea
                if linea:
                    print(f"Renviando dato completo: {linea}")

                    numero_destino = "***********"
                    cmd = f'AT+CMGS="{numero_destino}"\r\n'
                    ser.write(cmd.encode())
                    time.sleep(1)
                    resp = ser.read_all().decode(errors='ignore')
                    print("CMGS Response:", resp)

                    if '>' in resp:
                        #    Importante: no poner \r\n aquí, sino directamente \x1A
                        # Envías primera línea de texto
                        ser.write(f"Temperatura: {text}\r\n".encode())
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

                            # ser.write(dato)
    except KeyboardInterrupt:
        print("Programa detenido")

# Puca estuvo Aqui! 