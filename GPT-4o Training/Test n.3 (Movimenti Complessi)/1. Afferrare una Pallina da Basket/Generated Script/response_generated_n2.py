from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time
import numpy as np

def look_at(target):
    reachy.head.look_at(target[0], target[1], target[2], 1.0)

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

def grasp_ball():
    # Apertura della pinza
    reachy.r_arm.r_gripper.goal_position = -60  # Imposta la posizione di apertura

    # Aspetta un attimo per l'apertura
    time.sleep(1.0)

    # Posizione della pallina da basket
    ball_position = np.array([0.1, 0.3187999, -0.01479991])  # Coordinate della pallina da basket

    # Muovere il braccio verso la pallina
    move_arm(ball_position, duration=2.0)

    # Chiusura della pinza per afferrare la pallina
    reachy.r_arm.r_gripper.goal_position = -40  # Imposta la posizione di chiusura
    time.sleep(0.5)

    # Muovere il braccio leggermente verso l'alto per sollevare la pallina
    above_ball_position = np.array([0.1, 0.3187999, 0.1])  # Posizione sopra la pallina
    move_arm(above_ball_position, duration=2.0)

if __name__ == "__main__":
    # Connessione al robot Reachy
    reachy = ReachySDK(host='localhost')

    # Far guardare il robot verso la pallina
    look_at([0.1, 0.3187999, -0.01479991])  # Coordinate della pallina

    # Eseguire l'azione di afferraggio
    grasp_ball()

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

    # Uscire dal programma
    exit()