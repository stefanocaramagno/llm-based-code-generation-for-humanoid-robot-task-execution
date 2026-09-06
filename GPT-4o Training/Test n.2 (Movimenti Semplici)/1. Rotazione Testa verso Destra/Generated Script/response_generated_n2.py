from reachy_sdk import ReachySDK
import time

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Accendere la testa (se non è già accesa)
    reachy.turn_on('head')

    # Definire l'angolo di rotazione verso destra
    # Supponiamo di voler ruotare di 30 gradi a destra
    angle_to_rotate = 30  # in gradi

    # Ruotare la testa verso destra
    reachy.head.yaw.goal_position += angle_to_rotate

    # Impostare la durata del movimento
    duration = 1.0  # durata in secondi
    reachy.head.yaw.duration = duration

    # Avviare il movimento
    reachy.head.yaw.move()

    # Attendere che il movimento sia completato
    time.sleep(duration)

    # Spegnere la testa (opzionale)
    reachy.turn_off_smoothly('head')

    # Uscire dal programma
    exit()