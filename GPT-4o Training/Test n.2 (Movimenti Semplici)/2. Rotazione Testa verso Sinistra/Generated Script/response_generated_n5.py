from reachy_sdk import ReachySDK
import time

# Funzione per ruotare la testa verso sinistra
def rotate_head_left(reachy, angle, duration):
    # Posizione attuale della testa
    current_yaw = reachy.head.r_yaw.position
    target_yaw = current_yaw + angle  # Calcola la nuova posizione

    # Imposta la posizione obiettivo della testa
    reachy.head.r_yaw.goal_position = target_yaw
    reachy.head.r_yaw.goal_velocity = 0.5  # Imposta una velocità per il movimento

    # Attendere il completamento del movimento
    time.sleep(duration)

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Ruota la testa verso sinistra di 30 gradi in 1 secondo
    rotate_head_left(reachy, angle=-30, duration=1)

    # Ruota la testa indietro nella posizione originale
    rotate_head_left(reachy, angle=30, duration=1)

    # Spegnere la testa del robot in modo graduale
    reachy.turn_off_smoothly('head')

    # Uscire dal programma
    exit()