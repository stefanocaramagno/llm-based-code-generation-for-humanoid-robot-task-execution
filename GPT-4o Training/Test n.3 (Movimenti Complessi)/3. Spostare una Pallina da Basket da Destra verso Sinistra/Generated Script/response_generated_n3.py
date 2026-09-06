from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time
import numpy as np

# Funzione per muovere il braccio del robot verso una posizione target con una durata specificata
def move_arm(target, duration):
    # Creazione della matrice target per la cinematica inversa
    target_matrix = np.array([
        [0, 0, -1, target[0]],
        [0, 1, 0, target[1]],
        [1, 0, 0, target[2]],
        [0, 0, 0, 1],
    ])

    # Calcolo delle posizioni delle giunture usando la cinematica inversa
    joint_pos_ball = reachy.r_arm.inverse_kinematics(target_matrix)

    # Accensione del braccio destro
    reachy.turn_on('r_arm')

    # Movimento del braccio verso le posizioni delle giunture calcolate
    goto({joint: pos for joint, pos in zip(
         reachy.r_arm.joints.values(), joint_pos_ball)}, duration=duration)

# Funzione principale per spostare la pallina
def move_ball():
    # Coordinate iniziali della pallina a destra
    initial_ball_position = np.array([0.3187999 + 0.1, 0, -0.01479991])  # Aggiungi 10 cm a destra

    # Coordinate finali della pallina a sinistra
    final_ball_position = np.array([0.3187999 - 0.1, 0, -0.01479991])  # Sottrai 10 cm a sinistra

    # Muovere il braccio verso la posizione iniziale sopra la pallina
    move_arm(initial_ball_position, 2.0)
    time.sleep(1.0)

    # Muovere il braccio verso la posizione finale
    move_arm(final_ball_position, 2.0)
    time.sleep(1.0)

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il movimento della pallina
    move_ball()

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

    # Uscire dal programma
    exit()