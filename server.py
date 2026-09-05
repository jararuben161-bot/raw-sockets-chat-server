#se importan las bibliotecas
import socket
import threading
#se crea la lista de clientes
clientlist = []
#se crea la funcion de nuevo cliente donde entra un cliente, se le da un nombre, 
# puede enviar mensajes y puede ser eliminado sin interrumpir la conexion
def new_client(client_socket, addr):
    clientlist.append(client_socket)
    nombre = client_socket.recv(1024).decode("utf-8")
    try: 
     
      while True:
            msg = client_socket.recv(1024)
            if not msg:
                break
            print(str(nombre) + ">>" + msg.decode("utf-8"))
        
            mensaje_con_nombre = (nombre + ": " + msg.decode("utf-8")).encode("utf-8")
            for c in clientlist:
                if c != client_socket:
                    c.send(mensaje_con_nombre)
    except:
        pass
    finally:
        clientlist.remove(client_socket)
        client_socket.close()
        print (str(addr) + " ou la usuario")



#se crea el host y el port
HOST = "127.0.0.1"
PORT = 65123
#se crea el socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #TCP = Transmission Control Protocol
    #UDP = user datagram control
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    #setsocket=Te permite cambiar parámetros de bajo nivel, como el tamaño del búfer de memoria, los tiempos de espera (timeouts), o permitir ciertas conexiones especiales.
    #sol_socket =  Le avisa a la función setsockopt que la configuración que vas a modificar es general para el socket mismo, controlada por el sistema operativo
    # so_reuseaddr es una funcion que envia un true o false para reconectar en el bind
    s.bind((HOST, PORT))
    s.listen()
    while True:
     conn, addr = s.accept()
     print(f"OK,conexion hecha , EMPEZAR CHAT")
     threading.Thread(target=new_client, args=(conn, addr)).start()
   


#si se caen los server
#si hay dos servers
#funcion bloqueante
#explicar funcion with 