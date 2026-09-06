from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import numpy as np
import time

# Funzione per far guardare il robot verso un obiettivo
def look_at(target):
    reachy.head.look_at(target[0], target[1], target[2], 1.0)

# Funzione per muovere il braccio del robot verso una posizione target con una durata specificata
def move_arm(target, duration):
    target_matrix = np.array([
        [0, 0, -1, target[0]],
        [0, 1, 0, target[1]],
        [1, 0, 0, target[2]],
        [0, 0, 0, 1],
    ])

    joint_pos = reachy.r_arm.inverse_kinematics(target_matrix)
    reachy.turn_on('r_arm')
    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_pos)}, duration=duration)

# Funzione per afferrare la pallina
def grasp_ball():
    # Coordinate del tavolo
    table_position = np.array([0, 0.3187999, -0.01479991])  # Centro del tavolo

    # Calcolo della posizione della pallina (a destra e sopra il centro del tavolo)
    ball_position = np.array([table_position[0] + 0.1, table_position[1], table_position[2] + 0.05])  # Modifica le coordinate secondo necessità

    # Far guardare il robot verso la pallina
    look_at(ball_position)

    # Muovere il braccio sopra la pallina
    above_ball = np.array([ball_position[0], ball_position[1], ball_position[2] + 0.1])  # Posizione sopra la pallina
    move_arm(above_ball, 1.0)
    time.sleep(1.0)

    # Apertura della pinza
    reachy.r_arm.r_gripper.goal_position = -60  # Posizione per aprire la pinza
    time.sleep(1.0)

    # Raggiungere la pallina
    move_arm(ball_position, 2.0)
    time.sleep(2.0)

    # Chiusura della pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -40  # Posizione per chiudere la pinza
    time.sleep(0.5)

    # Alzare il braccio con la pallina
    move_arm(above_ball, 2.0)
    time.sleep(1.0)

    # Spegnere il braccio in modo graduale
    reachy.turn_off_smoothly('r_arm')

# Codice eseguibile principale
if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Eseguire il movimento di afferraggio
    grasp_ball()

    # Uscire dal programma
    exit()