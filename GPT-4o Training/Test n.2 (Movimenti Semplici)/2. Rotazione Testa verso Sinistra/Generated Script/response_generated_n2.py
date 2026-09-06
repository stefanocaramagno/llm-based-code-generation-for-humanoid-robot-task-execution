from reachy_sdk import ReachySDK
import time

def rotate_head_left(reachy, duration=1.0):
    # Ruota la testa a sinistra
    # Otteniamo la posizione attuale della testa
    current_head_yaw = reachy.head.r_yaw.position

    # Impostiamo un nuovo angolo per la rotazione a sinistra
    new_head_yaw = current_head_yaw - 30  # Ruota di 30 gradi a sinistra

    # Imposta la nuova posizione della testa
    reachy.head.r_yaw.goal_position = new_head_yaw
    reachy.head.r_yaw.goal_duration = duration

    # Accendi la testa
    reachy.turn_on('head')

    # Muovi la testa verso la nuova posizione
    reachy.head.goto(duration=duration)

    # Attendi il completamento del movimento
    time.sleep(duration)

    # Spegni la testa
    reachy.turn_off_smoothly('head')

if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Ruota la testa verso sinistra
    rotate_head_left(reachy, duration=1.0)