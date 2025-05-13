# MQTT para la BG96

Para los comandos AT con MQTT primero probe los comandos con Hercules.exe para poder ver la respuesta del modem a travez del  serial, probamos la configuracion incial 

```
AT
OK

AT+QCFG="band",f,8000008,8000008
OK


AT+QCFG="nwscanmode",3
OK


AT+QCFG="iotopmode",1
OK


AT+CFUN=0
OK
AT
OK


AT+CFUN=1
OK


AT+CPIN?
+CPIN: READY

OK


AT+COPS?
+COPS: 0,0,"Claro AR Claro AR",9

OK


AT+CSQ
+CSQ: 31,99

OK


AT+CGATT?
+CGATT: 1

OK


AT+QICSGP=1,1,"iot.claro.com.ar","","",1
OK


AT+QIACT=1
OK


AT+QIACT? 
+QIACT: 1,1,1,"000.000.000.000"

OK



AT+QPING=1,"test.mosquitto.org"
OK

+QPING: 0,"5.196.78.28",32,374,255

+QPING: 0,"5.196.78.28",32,405,255

+QPING: 0,"5.196.78.28",32,409,255

+QPING: 0,"5.196.78.28",32,430,255

+QPING: 0,4,4,0,374,430,403


AT+QMTOPEN=0,"test.mosquitto.org",1883
OK

+QMTOPEN: 0,0


AT+QMTCONN=0,"clienteBG96"
OK

+QMTCONN: 0,0,0
AT+QMTPUB=0,0,0,0,"ucc/temp",4
> 10

OK

+QMTPUB: 0,0,0
AT+QMTPUB=0,0,0,0,"ucc/temp",4
> 22.5
OK

+QMTPUB: 0,0,0
AT+QMTPUB=0,0,0,0,"ucc/temp",4
> 25

OK

+QMTPUB: 0,0,0
AT+QMTPUB=0,0,0,0,"ucc/temp",4
> 38

OK

+QMTPUB: 0,0,0
AT+QMTPUB=0,0,0,0,"ucc/temp",4
> 50

OK

+QMTPUB: 0,0,0

```

### **Configuración de bandas**
Este comando configura 2G en cualquier banda, CatM con B28, y NB-IoT con B4 y B28 
respectivamente; de no requerir alguna de las tecnologías se puede simplemente suprimir el 
campo

>AT+QCFG="band",f,8000008,8000008
>OK

### **Confugurar Tecnologias**

AT+QCFG="nwscanmode",3  --> _3 Para LTE con NB/LTE-m_
OK


AT+QCFG="iotopmode",1  --> _Solo para NB-IoT_
OK

### **Riniciamos el Modem BG-96 para afianzar los cambios**
AT+CFUN=0
OK

AT+CFUN=1
OK

### **Consultar Operador y SIM**
AT+CPIN?  --> _Consulta SIM_
+CPIN: READY
OK

AT+COPS?  --> _Consulta Operador_ 
+COPS: 0,0,"Claro AR Claro AR",9
OK


### **Configuracion del APN**


AT+QICSGP=1,1,"iot.claro.com.ar","","",1 --> _Aqui va la APN del Operador_
OK

AT+QIACT=1
OK


AT+QIACT? ---> _Deberiamos ver la IP asignada_
+QIACT: 1,1,1,"000.000.000.000"

OK

### **Prueba hacer ping al servidor**

AT+QPING=1,"test.mosquitto.org"

>[!HELP] Estamos utilizando "https://test.mosquitto.org/" un servidor MQTT publico, con el puerto 1883 que no tiene contraseña ni cifrado mas informacion en su pagina-


###**Abrimos Socket** 

AT+QMTOPEN=0,"test.mosquitto.org",1883

El comando AT+QIOPEN nos permite abrir conexiones tanto TCP como UDP, _en este caso por defecto TCP_.


### **Nos definimos como cliente MQTT**
AT+QMTCONN=0,"clienteBG96

_AT+QMTCONN=<tcpconnectID>,“<clientID>”[,“<username>”[,“<password>”]]_

<tcpconnectID>  MQTT socket identifier. The range is 0-5. 
<clientID>   The client identifier string. 
<username>      User name of the client. It can be used for authentication. 
<password>        Password corresponding to the user name of the client. It can be used for     


### **Publicamos Mensajes**
AT+QMTPUB=0,0,0,0,"ucc/temp",4

AT+QMTPUB=<tcpconnectID>,<msgID>,<qos>,<retain>,“<topic>”

<tcpconnectID>   MQTT socket identifier. The range is 0-5. 
<msgID>Message identifier of packet. The range is 0-65535.

**It will be 0 only when <qos>=0 COMO EN ESTA PRUBA**


