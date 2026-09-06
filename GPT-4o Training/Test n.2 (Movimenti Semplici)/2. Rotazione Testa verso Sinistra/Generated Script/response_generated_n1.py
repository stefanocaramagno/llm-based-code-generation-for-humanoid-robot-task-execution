from reachy_sdk import ReachySDK
import time

# Funzione per far ruotare la testa di Reachy verso sinistra
def rotate_head_left(reachy, angle, duration):
    # Imposta l'angolo della testa
    reachy.head.yaw.goal_position = -angle
    reachy.head.pitch.goal_position = 0  # Mantieni l'angolo di pitch a 0 per una rotazione piana

    # Accensione della testa
    reachy.turn_on('head')

    # Movimento della testa verso la posizione obiettivo
    reachy.head.goto(duration=duration)

    # Attendere il completamento del movimento
    time.sleep(duration)

if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Definire l'angolo di rotazione e la durata
    angle = 30  # Angolo di rotazione a sinistra in gradi
    duration = 1.0  # Durata del movimento in secondi

    # Eseguire la rotazione della testa verso sinistra
    rotate_head_left(reachy, angle, duration)

    # Spegnere la testa gradualmente
    reachy.turn_off_smoothly('head')

    # Uscire dal programma
    exit()