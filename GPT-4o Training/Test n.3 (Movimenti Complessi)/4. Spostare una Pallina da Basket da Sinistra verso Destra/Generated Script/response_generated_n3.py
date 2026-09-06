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

    joint_positions = reachy.r_arm.inverse_kinematics(target_matrix)
    reachy.turn_on('r_arm')

    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_positions)}, duration=duration)

# Funzione principale per spostare la pallina
def move_ball():
    # Coordinate della palla (iniziale)
    ball_position_start = np.array([0.3187999, -0.01479991, -1.204])  # Posizione iniziale della palla

    # Coordinate della palla (finale) spostata a destra
    ball_position_end = np.array([0.4187999, -0.01479991, -1.204])  # Aggiungi 10 cm a x

    # Far guardare il robot verso la palla
    reachy.head.look_at(ball_position_start[0], ball_position_start[1], ball_position_start[2], duration=1.0)
    time.sleep(1)

    # Muovere il braccio verso la posizione iniziale della palla
    move_arm(ball_position_start, duration=2.0)
    time.sleep(1)

    # Chiusura della pinza per afferrare la palla
    reachy.r_arm.r_gripper.goal_position = -40  # Regola la posizione della pinza per afferrare
    time.sleep(1)

    # Muovere il braccio verso la posizione finale della palla
    move_arm(ball_position_end, duration=2.0)
    time.sleep(1)

    # Apertura della pinza per rilasciare la palla
    reachy.r_arm.r_gripper.goal_position = -60  # Regola la posizione della pinza per rilasciare
    time.sleep(1)

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