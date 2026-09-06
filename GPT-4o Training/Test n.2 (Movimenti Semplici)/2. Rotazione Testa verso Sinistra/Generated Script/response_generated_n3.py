from reachy_sdk import ReachySDK
import time

# Funzione per ruotare la testa di Reachy verso sinistra
def rotate_head_left(reachy, angle):
    # Ruotare la testa verso sinistra
    reachy.head.yaw.goal_position = reachy.head.yaw.current_position + angle
    reachy.head.move_blocking()

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Angolo di rotazione verso sinistra in gradi
    angle = -30  # Ad esempio, ruotare di -30 gradi

    # Eseguire la rotazione della testa verso sinistra
    rotate_head_left(reachy, angle)

    # Attendere un momento per visualizzare la posizione finale
    time.sleep(2)

    # Spegnere la testa del robot in modo graduale
    reachy.turn_off_smoothly('head')

    # Uscire dal programma
    exit()