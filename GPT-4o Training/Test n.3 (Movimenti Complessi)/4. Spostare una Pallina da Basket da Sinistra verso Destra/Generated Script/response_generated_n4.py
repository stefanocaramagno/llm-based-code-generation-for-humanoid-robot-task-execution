from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time
import numpy as np

# Funzione per muovere il braccio del robot verso una posizione target con una durata specificata
def move_arm(target, duration):
    target_matrix = np.array([
        [0, 0, -1, target[0]],
        [0, 1, 0, target[1]],
        [1, 0, 0, target[2]],
        [0, 0, 0, 1],
    ])

    joint_pos_ball = reachy.r_arm.inverse_kinematics(target_matrix)

    reachy.turn_on('r_arm')

    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_pos_ball)}, duration=duration)

# Funzione per eseguire il movimento di presa e spostamento della pallina
def move_ball():
    # Coordinate della pallina da basket rispetto al sistema di riferimento di Reachy
    ball_position = np.array([-0.1, 0.3187999, -0.01479991])  # Un po' a sinistra del centro del tavolo
    above_ball = np.array([-0.1, 0.3187999, 0.1])  # Posizione sopra la pallina per afferrarla
    right_position = np.array([0.1, 0.3187999, -0.01479991])  # Posizione a destra del tavolo per spostare la pallina

    # Muovere il braccio sopra la pallina
    move_arm(above_ball, 1.0)
    time.sleep(1.0)

    # Raggiungere la pallina
    move_arm(ball_position, 2.0)
    time.sleep(2.0)

    # Apertura della pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -40  # Chiudere la pinza
    time.sleep(0.5)

    # Muovere il braccio a destra
    move_arm(right_position, 2.0)
    time.sleep(2.0)

    # Rilasciare la pallina
    reachy.r_arm.r_gripper.goal_position = -60  # Aprire la pinza
    time.sleep(0.5)

    # Tornare alla posizione iniziale
    move_arm(above_ball, 1.0)
    time.sleep(1.0)

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il movimento di spostamento della pallina
    move_ball()

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

    # Uscire dal programma
    exit()