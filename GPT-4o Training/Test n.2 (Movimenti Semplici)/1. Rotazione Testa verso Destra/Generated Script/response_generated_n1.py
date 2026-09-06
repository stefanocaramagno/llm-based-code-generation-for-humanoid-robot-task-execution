from reachy_sdk import ReachySDK
import time

def rotate_head_right(reachy, angle=30, duration=1.0):
    """
    Ruota la testa di Reachy verso destra di un certo angolo.

    :param reachy: istanza di ReachySDK
    :param angle: angolo di rotazione in gradi (default: 30)
    :param duration: durata del movimento in secondi (default: 1.0)
    """
    # Imposta la posizione della testa per ruotare verso destra
    current_yaw = reachy.head.r_head_yaw.position  # Ottieni la posizione attuale della testa
    target_yaw = current_yaw + angle  # Calcola la nuova posizione della testa

    # Muovi la testa verso la nuova posizione
    reachy.head.look_at(0, 0, 0, duration)  # Riferimento per la posizione, qui usiamo (0, 0, 0) per focalizzarci su un punto frontale
    reachy.head.r_head_yaw.goal_position = target_yaw  # Imposta la nuova posizione di yaw
    reachy.head.move(duration=duration)  # Esegui il movimento

if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Ruota la testa verso destra
    rotate_head_right(reachy, angle=30, duration=1.0)

    # Attendi qualche secondo per visualizzare il movimento
    time.sleep(2)

    # Spegnere il robot in modo sicuro
    reachy.turn_off_smoothly('head')