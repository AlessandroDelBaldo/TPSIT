import socket

# Configurazione del server
SERVER_ADDRESS = ('localhost', 9999)
BUFFER_SIZE = 4096

def avvia_server():
    # Crea il socket del server (IPv4, TCP)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Permette di riutilizzare l'indirizzo anche se già in uso (evita conflitti dopo riavvii rapidi)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Associa il socket all'indirizzo e alla porta
    server_socket.bind(SERVER_ADDRESS)
    
    # Mette il server in ascolto (max 5 connessioni in coda)
    server_socket.listen(5)
    
    print(f"Server TCP avviato su {SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}")
    print("In attesa di connessioni...")
    print("-" * 60)
    
    try:
        while True:
            # Accetta una connessione dal client
            client_socket, client_address = server_socket.accept()
            print(f"\nConnessione accettata da {client_address[0]}:{client_address[1]}")
            
            try:
                # Riceve il messaggio dal client
                messaggio_ricevuto = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                print(f"Messaggio ricevuto: '{messaggio_ricevuto}'")
                
                # Prepara la risposta
                risposta = f"Server ha ricevuto: {messaggio_ricevuto}"
                
                # Invia la risposta al client
                client_socket.sendall(risposta.encode('utf-8'))
                print(f"Risposta inviata: '{risposta}'")
                
            except Exception as e:
                print(f"Errore durante la comunicazione: {e}")
            
            finally:
                # Chiude la connessione con il client
                client_socket.close()
                print(f"Connessione chiusa con {client_address[0]}:{client_address[1]}")
                print("-" * 60)
    
    except KeyboardInterrupt:
        print("\nServer interrotto dall'utente")
    
    finally:
        # Chiude il socket del server
        server_socket.close()
        print("Server chiuso.")

if __name__ == "__main__":
    avvia_server()