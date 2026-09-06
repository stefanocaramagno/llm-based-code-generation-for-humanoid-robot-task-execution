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

    joint_pos_ball = reachy.r_arm.inverse_kinematics(target_matrix)
    reachy.turn_on('r_arm')

    goto({joint: pos for joint, pos in zip(reachy.r_arm.joints.values(), joint_pos_ball)}, duration=duration)

def basketball_movement():
    # Coordinate del tavolo
    table_position = np.array([0.3187999, 0, -1.204])

    # Posizione iniziale della palla (un po' a sinistra e sopra il centro del tavolo)
    ball_position_initial = np.array([table_position[0] - 0.2, table_position[1], table_position[2] + 0.1])

    # Posizione finale della palla (verso destra)
    ball_position_final = np.array([table_position[0] + 0.2, table_position[1], table_position[2] + 0.1])

    # Far guardare il robot verso la palla iniziale
    look_at(ball_position_initial)
    time.sleep(1)

    # Muovere il braccio verso la posizione iniziale della palla
    move_arm(ball_position_initial, 2.0)
    time.sleep(1)

    # Apertura della pinza per afferrare la palla
    reachy.r_arm.r_gripper.goal_position = -50
    time.sleep(1)

    # Rimanere un attimo in posizione
    time.sleep(1)

    # Muovere il braccio verso la posizione finale della palla
    move_arm(ball_position_final, 2.0)
    time.sleep(1)

    # Chiusura della pinza per rilasciare la palla
    reachy.r_arm.r_gripper.goal_position = -60
    time.sleep(1)

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

if __name__ == "__main__":
    reachy = ReachySDK(host='localhost')

    basketball_movement()

    # Uscire dal programma
    exit()