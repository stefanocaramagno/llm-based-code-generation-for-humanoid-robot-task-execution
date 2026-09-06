from reachy_sdk import ReachySDK
import time

# Funzione per ruotare la testa a sinistra
def rotate_head_left(reachy, angle=15, duration=1.0):
    # Ottieni la posizione attuale della testa
    current_yaw = reachy.head.r_arm_yaw.position

    # Calcola la nuova posizione per ruotare a sinistra
    new_yaw = current_yaw + angle

    # Imposta la nuova posizione della testa
    reachy.head.r_arm_yaw.goal_position = new_yaw

    # Muovi la testa verso la nuova posizione
    reachy.head.r_arm_yaw.move(duration=duration)

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Ruota la testa verso sinistra
    rotate_head_left(reachy, angle=15, duration=1.0)

    # Attendi un momento per osservare la posizione finale
    time.sleep(2)

    # Spegnere la testa del robot in modo graduale
    reachy.turn_off_smoothly('head')

    # Uscire dal programma
    exit()