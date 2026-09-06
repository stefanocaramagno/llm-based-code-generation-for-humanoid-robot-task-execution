from reachy_sdk import ReachySDK
import time

def rotate_head_right(reachy, angle):
    # Ottieni la posizione corrente della testa
    current_head_position = {
        'head_yaw': reachy.head.head_yaw.position,
        'head_pitch': reachy.head.head_pitch.position,
    }

    # Calcola la nuova posizione della testa ruotando a destra
    new_head_position = {
        'head_yaw': current_head_position['head_yaw'] + angle,
        'head_pitch': current_head_position['head_pitch'],
    }

    # Muovi la testa verso la nuova posizione
    reachy.head.goto(new_head_position, duration=1.0)

if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Ruota la testa a destra di 30 gradi
    rotate_head_right(reachy, angle=30)

    # Attendere un momento per osservare il movimento
    time.sleep(2)

    # Spegnere il sistema
    reachy.turn_off_smoothly('head')