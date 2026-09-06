from reachy_sdk import ReachySDK
import time

# Funzione per ruotare la testa a destra
def rotate_head_right(reachy, angle):
    # Definiamo la posizione attuale della testa
    current_position = reachy.head.get_joint_angles()

    # Aggiungiamo l'angolo desiderato (in gradi) all'angolo di yaw
    new_yaw = current_position[reachy.head.joints['head_yaw']] + angle

    # Aggiorniamo la posizione della testa
    reachy.head.goal_position = {
        reachy.head.joints['head_yaw']: new_yaw,
        reachy.head.joints['head_pitch']: current_position[reachy.head.joints['head_pitch']]  # Manteniamo l'angolo di pitch invariato
    }

    # Eseguiamo il movimento
    reachy.head.goto(duration=1.0)  # Durata di 1 secondo per la transizione

if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Accensione della testa
    reachy.turn_on('head')

    # Ruotare la testa a destra di 30 gradi
    rotate_head_right(reachy, 30)

    # Attendere un momento per osservare la posizione finale
    time.sleep(2)

    # Spegnere la testa
    reachy.turn_off_smoothly('head')

    # Uscire dal programma
    exit()