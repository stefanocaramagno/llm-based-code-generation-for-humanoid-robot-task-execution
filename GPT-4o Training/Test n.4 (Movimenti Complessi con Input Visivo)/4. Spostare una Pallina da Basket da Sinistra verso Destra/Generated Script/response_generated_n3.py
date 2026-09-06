from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import numpy as np
import time

# Inizializza la connessione al robot Reachy
reachy = ReachySDK(host='localhost')

# Funzione per muovere il braccio del robot verso una posizione target
def move_arm(target, duration):
    # Creazione della matrice target per la cinematica inversa
    target_matrix = np.array([
        [0, 0, -1, target[0]],
        [0, 1, 0, target[1]],
        [1, 0, 0, target[2]],
        [0, 0, 0, 1],
    ])

    # Calcolo delle posizioni delle giunture usando la cinematica inversa
    joint_pos = reachy.r_arm.inverse_kinematics(target_matrix)

    # Accensione del braccio destro
    reachy.turn_on('r_arm')

    # Movimento del braccio verso le posizioni delle giunture calcolate
    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_pos)}, duration=duration)

# Funzione principale per spostare la pallina da basket
def move_basketball():
    # Coordinate iniziali della pallina da basket (a sinistra rispetto al centro)
    ball_position_start = np.array([-0.5, 0.3187999, -0.01479991])  # A sinistra
    # Coordinate finali della pallina da basket (a destra rispetto al centro)
    ball_position_end = np.array([0.5, 0.3187999, -0.01479991])    # A destra

    # Muovere il braccio sopra la palla iniziale
    move_arm(ball_position_start, duration=2.0)
    time.sleep(1.0)  # Attendere che il movimento sia completato

    # Apertura della pinza per afferrare la palla
    reachy.r_arm.r_gripper.goal_position = -50  # Apri la pinza
    time.sleep(1.0)  # Attendere che la pinza si apra

    # Muovere il braccio verso la posizione della palla
    move_arm(ball_position_start, duration=1.0)
    time.sleep(2.0)  # Attendere che il movimento sia completato

    # Chiusura della pinza per afferrare la palla
    reachy.r_arm.r_gripper.goal_position = -20  # Chiudi la pinza
    time.sleep(0.5)  # Attendere che la pinza si chiuda

    # Muovere il braccio verso la posizione finale (a destra)
    move_arm(ball_position_end, duration=2.0)
    time.sleep(1.0)  # Attendere che il movimento sia completato

    # Apertura della pinza per rilasciare la palla
    reachy.r_arm.r_gripper.goal_position = -50  # Apri la pinza
    time.sleep(1.0)  # Attendere che la pinza si apra

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

# Eseguire la funzione principale
if __name__ == "__main__":
    move_basketball()