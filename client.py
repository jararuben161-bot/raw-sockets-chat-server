#se importan las bibliotecas
import socket
import threading
import time
#se crea el host y el port
HOST = "127.0.0.1"
PORT = 65123

#se establece una conexion como una alarma
conectado = False
#se crea la funcion recibir donde se espera
#que reciba los mensajes
def recibir(s):
    global conectado
   
    while True:
        try:
            msg = s.recv(1024)
            if not msg:
                break
            print(msg.decode("utf-8"))
        except:
            break
    conectado = False
#funcion de enviar donde se espera que envie los mensaje
def enviar(s):
    global conectado
    while conectado:
        msg = input()
        try:
            s.send(msg.encode("utf-8"))
        except:
            conectado = False
            break
#se crea la funcion cliente, donde se le conecta al cliente al servidor
#  mensaje donde el usuario se pone un nombre y
# se puede volver a reconectar y todo el sistema espera 
def cliente():
    global conectado
    nombre = input (" buenos dias, cual es tu nombre? ")
    while True:
     while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((HOST, PORT))
                print("OK,conectado al servidor, CHAT INICIADO")
                s.send(nombre.encode("utf-8"))
                break 
            except ConnectionRefusedError:
                print("servidor no disponible, reintentando en 3 segundos...")
                time.sleep(3)
            
     conectado = True
     hilo_recibir = threading.Thread(target=recibir, args=(s,))
     hilo_recibir.start()
     threading.Thread(target=enviar, args=(s,)).start()
     hilo_recibir.join()  # espera hasta que se caiga
        
     print("conexión perdida, volviendo a intentar")
     time.sleep(3)

cliente()


# detectar fallas del cosigo y hacer que funcione
# Implementar un saludo inicial donde el cliente 
# envía su nombre al conectarse y debe esperar 
# un "OK" del servidor antes de habilitar el chat.