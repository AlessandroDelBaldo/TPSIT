import socket

# Configurazione del client
SERVER_ADDRESS = ('localhost', 9999)
BUFFER_SIZE = 4096

def main():
    # 1. Crea il socket del client
    print("Creazione del socket...")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket creato con successo")
    
    try:
        # 2. Connessione al server
        print(f"\nConnessione al server {SERVER_ADDRESS[0]}:{SERVER_ADDRESS[1]}...")
        client_socket.connect(SERVER_ADDRESS)
        print("Connesso al server")
        
        # 3. Preparazione del messaggio da inviare
        messaggio = input("\nInserisci il messaggio da inviare al server: ")
        
        # 4. Invio del messaggio al server
        print(f"\nInvio del messaggio: '{messaggio}'")
        client_socket.sendall(messaggio.encode('utf-8'))
        print("Messaggio inviato")
        
        # 5. Ricezione della risposta dal server
        print("\nRicezione della risposta dal server...")
        risposta = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        print(f"Risposta ricevuta: '{risposta}'")
        
    except ConnectionRefusedError:
        print("\nERRORE: Impossibile connettersi al server.")
        print("Assicurati che il server sia in esecuzione.")
    
    except Exception as e:
        print(f"\nERRORE: {e}")
    
    finally:
        # 6. Chiusura del socket
        print("\nChiusura della connessione...")
        client_socket.close()
        print("Connessione chiusa")

if __name__ == "__main__":
    print("=" * 60)
    print("CLIENT TCP - Esercizio Base")
    print("=" * 60)
    main()
    print("\n" + "=" * 60)
    print("Programma terminato")
    print("=" * 60)