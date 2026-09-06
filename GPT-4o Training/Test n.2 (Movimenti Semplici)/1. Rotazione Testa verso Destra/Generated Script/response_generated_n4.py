from reachy_sdk import ReachySDK
import time

# Funzione per ruotare la testa del robot verso destra
def rotate_head_right(angle):
    # Impostare l'angolo di rotazione per la testa
    reachy.head.r_head_yaw.goal_position += angle

    # Muovere la testa verso la posizione desiderata
    reachy.head.move_sync(duration=1.0)  # Durata del movimento in secondi

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Ruotare la testa verso destra di un angolo di 30 gradi (puoi cambiare questo valore)
    rotate_head_right(angle=30)

    # Attendere un momento per osservare il movimento
    time.sleep(2)

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

    # Uscire dal programma
    exit()