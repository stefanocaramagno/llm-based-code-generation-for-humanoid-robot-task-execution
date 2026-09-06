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

# Funzione principale per spostare la palla da destra a sinistra
def move_ball():
    # Coordinate della pallina da basket (iniziali)
    ball_position_start = np.array([0.3187999, -0.01479991, -1.204])  # Posizione iniziale a destra
    # Coordinate della pallina da basket (finali)
    ball_position_end = np.array([-0.3187999, -0.01479991, -1.204])  # Posizione finale a sinistra

    # Muovere il braccio sopra la pallina
    move_arm(ball_position_start, duration=2.0)
    time.sleep(1)  # Attendere che il braccio si posizioni

    # Chiusura della pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -40  # Regola l'apertura della pinza
    time.sleep(0.5)

    # Muovere il braccio verso la posizione finale
    move_arm(ball_position_end, duration=2.0)
    time.sleep(1)  # Attendere che il braccio si posizioni

    # Apertura della pinza per rilasciare la pallina
    reachy.r_arm.r_gripper.goal_position = -60  # Aumenta l'apertura della pinza
    time.sleep(0.5)

    # Spegnere il braccio destro in modo graduale
    reachy.turn_off_smoothly('r_arm')

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il movimento della palla
    move_ball()

    # Uscire dal programma
    exit()