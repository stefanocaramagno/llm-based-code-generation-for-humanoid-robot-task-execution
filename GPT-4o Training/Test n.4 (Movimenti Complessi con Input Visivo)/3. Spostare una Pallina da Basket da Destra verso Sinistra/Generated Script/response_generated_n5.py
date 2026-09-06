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
    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_pos_ball)}, duration=duration)

# Funzione principale per spostare la pallina da basket
def move_basketball():
    # Posizione iniziale della pallina da basket (a destra del centro del tavolo)
    ball_position_start = np.array([0.1, 0.3187999, -0.01479991])  # Esempio di coordinate
    # Posizione finale della pallina da basket (a sinistra del centro del tavolo)
    ball_position_end = np.array([-0.1, 0.3187999, -0.01479991])  # Esempio di coordinate

    # Muovere il braccio sopra la pallina per afferrarla
    above_ball = np.array([ball_position_start[0], ball_position_start[1], ball_position_start[2] + 0.1])
    move_arm(above_ball, 2.0)

    # Apertura della pinza
    reachy.r_arm.r_gripper.goal_position = -60
    time.sleep(1.0)

    # Raggiungere la pallina
    move_arm(ball_position_start, 2.0)
    time.sleep(2.0)

    # Chiusura della pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -40
    time.sleep(0.5)

    # Alzare il braccio con la pallina
    move_arm(above_ball, 2.0)
    time.sleep(1.0)

    # Muovere la pallina da destra a sinistra
    move_arm(ball_position_end, 2.0)
    time.sleep(2.0)

    # Rilasciare la pallina
    reachy.r_arm.r_gripper.goal_position = -60
    time.sleep(1.0)

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il movimento di spostamento della pallina da basket
    move_basketball()

    # Uscire dal programma
    exit()