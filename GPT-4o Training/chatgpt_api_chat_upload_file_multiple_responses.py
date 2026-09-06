import openai
import os

# Imposta la tua chiave API
openai.api_key = "sk-example"

# Inizializza il contesto della conversazione
messages = [
    {"role": "system", "content": "Sei un esperto di algoritmi di programmazione per robot antropomorfi."},
]

# Funzione per leggere il contenuto di un file
def leggi_file(file_path):
    try:
        # Controlla l'estensione del file per decidere se leggerlo come testo o binario
        _, estensione = os.path.splitext(file_path)
        if estensione.lower() in ['.jpg', '.png', '.jpeg', '.bmp', '.gif']:  # File binari (immagini)
            with open(file_path, "rb") as file:
                return f"Contenuto binario del file {file_path}: {len(file.read())} byte"
        else:  # File di testo
            with open(file_path, "r", encoding="utf-8") as file:
                return file.read()
    except FileNotFoundError:
        return f"File non trovato: {file_path}"
    except UnicodeDecodeError:
        return f"Errore di decodifica del file di testo: {file_path}"

# Ciclo per inviare messaggi all'assistente
while True:
    message = input("User: ")
    
    # Esci dal ciclo se l'utente digita "esci"
    if message.lower() == "esci":
        print("Chat terminata.")
        break

    # Se l'utente digita "allega file", chiedi uno o più percorsi dei file e leggi i contenuti
    if message.lower() == "allega file":
        file_paths = input("Inserisci i percorsi dei file separati da virgola: ").split(',')
        file_contents = []

        # Leggi ciascun file e aggiungi il contenuto
        for file_path in file_paths:
            file_content = leggi_file(file_path.strip())
            file_contents.append(file_content)

        # Combina i contenuti dei file
        message = f"Ecco i contenuti dei file:\n\n" + "\n\n".join(file_contents)

        # Aggiungi il messaggio dell'utente
        messages.append({"role": "user", "content": message})

        # Invio della richiesta al modello GPT-4o mini con una singola risposta (nessuna risposta multipla)
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7  # Parametro di variabilità
        )
        
        # Ottieni la singola risposta
        reply = response['choices'][0]['message']['content']
        print(f"ChatGPT-4o mini: {reply}")
        
        # Aggiungi la risposta dell'assistente al contesto
        messages.append({"role": "assistant", "content": reply})

    else:
        # Per altri messaggi (non allega file), invia una richiesta con 5 risposte multiple
        messages.append({"role": "user", "content": message})

        # Invio della richiesta al modello GPT-4o mini con 5 risposte multiple
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            n=5,  # Genera 5 risposte multiple
            temperature=0.7,  # Parametro di variabilità
            top_p=0.9
        )
        
        # Itera su ciascuna risposta
        for i, choice in enumerate(response['choices']):
            reply = choice['message']['content']
            print(f"\nRisposta {i + 1}:\n{reply}\n")
            
            # Aggiungi ciascuna risposta dell'assistente al contesto
            messages.append({"role": "assistant", "content": reply})
