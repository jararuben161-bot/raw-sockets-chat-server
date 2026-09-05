''' COMPLETA LA FUNCION FALTANTE '''

import socket
import threading

# --- Configuración del servidor ---
HOST = '127.0.0.1'
PORT = 12345

# --- Lista global de clientes conectados ---
clientes_conectados = []
clientes_lock = threading.Lock()  # Para evitar errores de concurrencia


def crear_socket_servidor():
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((HOST, PORT))
    servidor.listen()
    print(f"[+] Servidor escuchando en {HOST}:{PORT}")
    return servidor


# --- Función para enviar mensaje a todos los demás clientes ---
#-----------------------------------------------------------------------------------
def broadcast(mensaje, cliente_emisor):
# funcion broadcast(mensaje, cliente_emisor):
    # Bloquear el acceso a la lista de clientes para evitar errores de concurrencia
    with clientes_lock:
        for  c in clientes_conectados():
            if cliente_emisor != c :
                try:
                    c.send(mensaje.encode("utf-8"))
                except:
                    c.close()
                    clientes_conectados.remove(c)
        # Recorrer todos los clientes conectados
            # Si el cliente no es el que envió el mensaje

                #intenta:
                    # Enviar el mensaje codificado en UTF-8 al cliente

                #exepto:
                    # Si ocurre un error, cerrar el socket y eliminarlo de la lista
                    # Cerrar el socket del cliente
                    # Remover el cliente de la lista
        pass
#-----------------------------------------------------------------------------------


# --- Función para manejar a un cliente ---
def manejar_cliente(socket_cliente, direccion_cliente):
    print(f"[+] Nueva conexión desde {direccion_cliente}")

    with clientes_lock:
        clientes_conectados.append(socket_cliente)

    try:
        while True:
            mensaje = socket_cliente.recv(1024).decode('utf-8')
            if not mensaje:
                break  # Cliente cerró conexión
            print(f"[{direccion_cliente}] {mensaje}")
             broadcast(f"[{direccion_cliente}] {mensaje}", socket_cliente)
    except ConnectionResetError:
        pass  # Cliente se desconectó forzadamente
    finally:
        with clientes_lock:
            if socket_cliente in clientes_conectados:
                clientes_conectados.remove(socket_cliente)
        socket_cliente.close()
        print(f"[-] Cliente desconectado: {direccion_cliente}")

# --- Función principal para iniciar el servidor ---
def iniciar_servidor():
    servidor = crear_socket_servidor()

    while True:
        socket_cliente, direccion = servidor.accept()
        hilo = threading.Thread(target=manejar_cliente, args=(socket_cliente, direccion))
        hilo.start()

# --- Punto de entrada ---
if __name__ == "__main__":
    iniciar_servidor()