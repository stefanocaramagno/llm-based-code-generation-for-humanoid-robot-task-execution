from reachy_sdk import ReachySDK
from reachy_sdk.trajectory import goto
from reachy_sdk.trajectory import InterpolationMode
import time
import numpy as np

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

    joint_pos_ball = reachy.r_arm.inverse_kinematics(target_matrix)
    reachy.turn_on('r_arm')

    goto({joint: pos for joint, pos in zip(
         reachy.r_arm.joints.values(), joint_pos_ball)}, duration=duration)

# Funzione per afferrare la pallina
def grasp_ball(ball_position):
    # Apertura della pinza
    reachy.r_arm.r_gripper.goal_position = -60  # Apertura
    time.sleep(1.0)  # Attendere che la pinza si apra

    # Muovere il braccio verso la pallina
    move_arm(ball_position, 2.0)
    time.sleep(2.0)  # Attendere il completamento del movimento

    # Chiusura della pinza
    reachy.r_arm.r_gripper.goal_position = -40  # Chiusura
    time.sleep(1.0)  # Attendere che la pinza si chiuda

# Funzione principale per il grasping
def main():
    # Connessione al robot Reachy
    global reachy
    reachy = ReachySDK(host='localhost')

    # Coordinate della pallina da basket (un po' più a destra e sopra il centro del tavolo)
    ball_position = np.array([0.1, 0.3187999 + 0.1, -0.01479991 + 0.2])  # (x, y, z)

    # Far guardare il robot verso la pallina
    look_at(ball_position)

    # Eseguire il movimento di grasping
    grasp_ball(ball_position)

    # Spegnere il braccio destro del robot in modo graduale
    reachy.turn_off_smoothly('r_arm')

if __name__ == "__main__":
    main()